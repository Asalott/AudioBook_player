# The library.py file
from pathlib import Path

import sqlite3 # imports the sqlite3 module to interact with the SQLite database

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# This function finds all .m4b files in the specified folder and its subfolders.
class BookLibrary: 
    def find_books(folder_path):
        """Finds all .m4b files in the specified folder and its subfolders.

        Args:
            folder_path (str): The path to the folder to search for .m4b files.
        """
        # Check if the folder exists and is a directory
        folder = Path(folder_path)
        if not folder.is_dir():
            print(f"Folder '{folder_path}' does not exist.")
            return []
        return sorted(str(path) for path in folder.rglob("*.m4b") if path.is_file())

    # This function creates a SQLite database to store book information.
    def create_database(db_path):
        """Creates a SQLite database to store book information.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                path TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

    # This function loads book information into the SQLite database.
    def load_books_into_database(db_path, books):
        """Loads book information into the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.
            books (list): A list of book file paths.
        """
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for book_path in books:
            title = Path(book_path).stem  # Use the file name without extension as the title
            author = "Unknown"  # Placeholder for author, can be updated later
            cursor.execute('''
                INSERT OR IGNORE INTO books (title, author, path)
                VALUES (?, ?, ?)
            ''', (title, author, book_path))
        conn.commit()
        conn.close()

    # This function retrieves all books from the SQLite database.
    def get_books_from_database(db_path):
        """Retrieves all books from the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT title, author, path FROM books')
        books = cursor.fetchall()
        conn.close()
        return books

    def enumerate_books(books):
        """Enumerates the books and prints them with their index.

        Args:
            books (list): A list of book information tuples.
        """
        for i, book in enumerate(books):
            print(f"{i}: {book}")

    # this function is used to get all the books in the folder and its subfolders and return them as a list of strings
    if __name__ == "__main__":
        books = find_books("books")
        if books:
            print("Found the following .m4b files:")
            for book in books:
                print(book)


