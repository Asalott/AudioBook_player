from flask import Flask, jsonify, send_from_directory, request
from pathlib import Path
from library import BookLibrary
from player import BookPlayer
import time
import sqlite3


app = Flask(__name__)
db = BookLibrary()

player = None

# this function gets the main page of the web application and returns the HTML file
@app.get("/")
def index():
    return send_from_directory(Path(__file__).parent, "bibliotek.html")

@app.get("/spelare.html")
def bibliotek():
    return send_from_directory(Path(__file__).parent, "spelare.html")

@app.post("/api/select-book")
def select_book():
    global player
    book_id = request.json.get("id")
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"status": "error", "message": "Book not found"}), 404
    path = row[0]
    player = BookPlayer(path)
    return jsonify({"status": "ok", "path": path})

@app.get("/api/books")
def get_books():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, path, cover_path FROM books")
    rows = cursor.fetchall()
    conn.close()
    books = [{"id": r[0], "title": r[1], "author": r[2], "path": r[3], "cover_path": r[4]} for r in rows]
    return jsonify(books)

# plays the book
@app.post("/api/play")
def play():
    if player is None:
        return jsonify({"status": "error", "message": "No book selected"}), 400
    player.play_book()
    return jsonify({"status": "playing"})

# pauses the book
@app.post("/api/pause")
def pause():
    player.pause_book()
    return jsonify({"status": "pause"})

# skips 10 secounds of the book
@app.get("/api/skip")
def skip():
    player.skip_forward(10000)
    return jsonify({"status": "skip"})

@app.get("/covers/<filename>")
def get_cover(filename):
    return send_from_directory(Path(__file__).parent / "covers", filename)

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
