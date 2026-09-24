# The library.py file
from pathlib import Path
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
                path TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()
        self.conn.close()

    # This function loads book information into the SQLite database.
    def load_books_into_database(self, db_path, books):
        """Loads book information into the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.
            books (list): A list of book file paths.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        for book_path in books:
            title = Path(book_path).stem  # Use the file name without extension as the title
            author = "Unknown"  # Placeholder for author, can be updated later
            self.cursor.execute('''
                INSERT OR IGNORE INTO books (title, author, path)
                VALUES (?, ?, ?)
            ''', (title, author, book_path))
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



