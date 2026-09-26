# The library.py file
from pathlib import Path
from mutagen.mp4 import MP4
import sqlite3 # imports the sqlite3 module to interact with the SQLite database
import re, subprocess, json

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# This function finds all .m4b files in the specified folder and its subfolders.
class BookLibrary: 
    def find_books(self, folder_path):
        """Finds all .m4b files in the specified folder and its subfolders.

        Args:
            folder_path (str): The path to the folder to search for .m4b files.
        """
        # Check if the folder exists and is a directory
        self.folder = Path(folder_path).resolve()
        if not self.folder.is_dir():
            print(f"Folder '{folder_path}' does not exist.")
            return []
        return sorted(str(path) for path in self.folder.rglob("*.m4b") if path.is_file())

    # This function creates a SQLite database to store book information.
    def create_database(self, db_path):
        """Creates a SQLite database to store book information.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                path TEXT NOT NULL UNIQUE,
                chapters TEXT,
                cover_path TEXT,
                last_position INTEGER DEFAULT 0
            )
        ''')
        try:
            self.cursor.execute("ALTER TABLE books ADD COLUMN last_position INTEGER DEFAULT 0")
            self.conn.commit()
        except sqlite3.OperationalError:
            pass  # kolumnen finns redan om databasen skapats tidigare
        self.conn.commit()

    def extract_cover_art(self, book_path, output_path):
        self.audio = MP4(book_path)
        self.covers = self.audio.tags.get("covr")
        if not self.covers:
            return None
        self.cover_data = self.covers[0]
        with open(output_path, "wb") as f:
            f.write(self.cover_data)
        return str(output_path)

    def clean_title(self, title):
        """Städar en boktitel för visning: tar bort ASIN-koder och konstiga tecken."""
        title = re.sub(r'\[[^\]]*\]', '', title)              # tar bort [B09CVBKH5L] osv
        title = re.sub(r'[^\w\s.,\'!?&:-]', '', title, flags=re.UNICODE)  # tar bort konstiga tecken
        title = re.sub(r'\s+', ' ', title).strip()             # städar mellanslag
        return title


    # This function loads book information into the SQLite database.
    def load_books_into_database(self, db_path, books):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        covers_dir = Path("covers")
        covers_dir.mkdir(exist_ok=True)

        for book_path in books:
            title = self.clean_title(Path(book_path).stem)
            author = "Unknown"

            cover_output = covers_dir / f"{Path(book_path).stem}.jpg"
            cover_path = self.extract_cover_art(book_path, cover_output)
            chapters = self.extract_chapters(book_path)

            self.cursor.execute('''
                INSERT OR IGNORE INTO books (title, author, path, chapters, cover_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, author, book_path, json.dumps(chapters), cover_path))
        self.conn.commit()

    # This function retrieves all books from the SQLite database.
    def get_books_from_database(self, db_path):
        """Retrieves all books from the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT title, author, path FROM books')
        books = self.cursor.fetchall()
        self.conn.close()
        return books

    def extract_chapters(self, book_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-i", book_path, "-print_format", "json", "-show_chapters", "-loglevel", "error"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True
            )
            data = json.loads(result.stdout)
            chapters = []
            for ch in data.get("chapters", []):
                chapters.append({
                    "title": ch.get("tags", {}).get("title", "Okänt kapitel"),
                    "start": float(ch.get("start_time", 0)),
                    "end": float(ch.get("end_time", 0))
                })
            return chapters
        except Exception as e:
            print(f"Kunde inte extrahera kapitel: {e}")
            return []
    
    # This function closes the database connection.
    def close_database(self):
        self.conn.close()



