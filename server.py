from flask import Flask, jsonify, send_from_directory
from pathlib import Path
import sqlite3

app = Flask(__name__)

# this function gets the main page of the web application and returns the HTML file
@app.get("/")
def index():
    return send_from_directory(Path(__file__).parent, "spelare.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
