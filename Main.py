# This is the main python file

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# import
import time
# imports the find_books function from library.py
from library import BookLibrary
# imports the BookPlayer class from player.py
from player import BookPlayer

# path to the SQLite database file
DB_PATH = "books.db"

# handles the main logic of the program, including finding books, creating a database, loading books into the database, and playing the selected book
library = BookLibrary()
books = library.find_books("books")  # finds all .m4b files in the specified folder and its subfolders

library.create_database("DB_PATH")  # creates a SQLite database to store book information

library.load_books_into_database("DB_PATH", books)  # loads book information into the SQLite database

library.enumerate_books(DB_PATH)  # enumerates the books in the database and prints them with their index

input_book = int(input("Input the number of the book you want to play: "))  # input from the user to select the book they want to play

player = BookPlayer(books[input_book])  # creates a BookPlayer object with the selected book

# input from the user to control the audio player hopefully it will be UI in the future
input_play = input("Input play if you want to play the book: ").strip().lower()

if input_book < len(books):  # checks if the input is valid and within the range of the books list
    # place holder vill be replaced with a UI in the future to control the audio player
    if input_play == "play":

        player.play_book()  # plays the book using the BookPlayer object
        
        # Optional: keep the loop running without blocking forever
        while True:
            # gets the current time of the book in milliseconds
            get_time = player.get_time()
            print(f"Current time: {get_time} ms")

            # place holder vill be replaced with a UI in the future to control the audio player
            input_pause = input(str("input pause if you want to pause the book:"))
            if input_pause == "pause":
                player.pause_book()  # pauses the book using the BookPlayer object

        print("Exiting the program.")
# will add proper error handling in the future to handle invalid input and other errors
elif input_book >= len(books):
    print("Invalid book selection. Exiting the program.")
