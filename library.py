# The library.py file
from pathlib import Path
from mutagen.mp4 import MP4
import sqlite3 # imports the sqlite3 module to interact with the SQLite database

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
                cover_path TEXT NOT NULL
            )
        ''')
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


    # This function loads book information into the SQLite database.
    def load_books_into_database(self, db_path, books):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        covers_dir = Path("covers")
        covers_dir.mkdir(exist_ok=True)

        for book_path in books:
            title = Path(book_path).stem
            author = "Unknown"

            cover_output = covers_dir / f"{Path(book_path).stem}.jpg"
            cover_path = self.extract_cover_art(book_path, cover_output)

            self.cursor.execute('''
                INSERT OR IGNORE INTO books (title, author, path, cover_path)
                VALUES (?, ?, ?, ?)
            ''', (title, author, book_path, cover_path))
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
    
    # This function closes the database connection.
    def close_database(self):
        self.conn.close()



