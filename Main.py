# This is the main python file

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# import
import time
# imports the find_books function from library.py
from library import BookLibrary
# imports the BookPlayer class from player.py
from player import BookPlayer
# imports the flask server app into the Main.py
from server import app

# handles the main logic of the program, including finding books, creating a database, loading books into the database, and playing the selected book
library = BookLibrary()
scan = library.find_books("books")  # finds all .m4b files in the specified folder and its subfolders

library.create_database("books.db")  # creates a SQLite database to store book information

library.load_books_into_database("books.db", scan)  # loads book information into the SQLite database

#get_book = library.get_books_from_database("books.db")

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)

input_book = int(input("Input the number of the book you want to play: "))  # input from the user to select the book they want to play

player = BookPlayer(scan[input_book])  # creates a BookPlayer object with the selected book

library.close_database()  # closes the database connection after loading the books into the database

player.play_book()  # plays the book using the BookPlayer object