# This is the main python file

# import
import vlc  # imports python-vlc
import time # imports time

# path to the book
book_path = 'books/The Eminence in Shadow, Vol. 5 [B0GQD2Z6TV]/The Eminence in Shadow, Vol. 5 [B0GQD2Z6TV].m4b'
print("Loading the book...")

# Designates the player
player = vlc.MediaPlayer(book_path)
print("Book loaded successfully.")

# plays the book
player.play()
print("Playing the book...")

time.sleep(1) # adds a delay to allow the player to start to get a proper length value

# gets the length of the book in milliseconds
get_length = player.get_length()
print(f"Book length: {get_length} ms")

time.sleep(get_length / 1000)  # plays the book for its entire length# This is the main python file
