# This is the main python file

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# import
import time
# imports the find_books function from library.py
from library import find_books

from player import BookPlayer

# time values in milliseconds for the audio player to only play the book for a certain amount of time
sixty_minutes = 3600000  # sixty minutes in seconds
forty_minutes = 2400000  # forty minutes in seconds
thirty_minutes = 1800000  # thirty minutes in seconds
fifteen_minutes = 900000  # fifteen minutes in seconds

# skip values in milliseconds for the audio player to skip forward or backward in the book
skip_10sec = 10000  # ten seconds in milliseconds

books = find_books("books")  # finds all the books in the books folder and its subfolders
for i, book in enumerate(books):  # enumerates the books and prints them with their index
    print(f"{i}: {book}")  # prints the index and the book path

input_book = int(input("Input the number of the book you want to play: "))  # input from the user to select the book they want to play

# input from the user to control the audio player hopefully it will be UI in the future
input_play = input("Input play if you want to play the book: ").strip().lower()

if input_play == "play":

    player = BookPlayer(books[input_book])  # creates a BookPlayer object with the selected book

    player.play_book()  # plays the book using the BookPlayer object
    
    # Optional: keep the loop running without blocking forever
    while True:
        # gets the current time of the book in milliseconds
        get_time = player.get_time()
        print(f"Current time: {get_time} ms")

        input_pause = input(str("input pause if you want to pause the book:"))
        if input_pause == "pause":
            player.pause_book()  # pauses the book using the BookPlayer object
            break  # exits the loop after pausing

        time.sleep(1)  # adds a delay to avoid excessive CPU usage
    print("Exiting the program.")

