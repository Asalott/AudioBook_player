# This is the player python file

# imports the vlc module to play audio files
import vlc 

# This is the player class that is used to play audio books using the VLC media player
class BookPlayer:
    # This class is used to play audio books using the VLC media player.
    def __init__(self, BookPath):
        self.book_path = BookPath
        self.player = vlc.MediaPlayer(self.book_path)

    # This function is used to play the book using the VLC media player
    def play_book(self):
        """Plays the book using the VLC media player."""
        self.player.play()
        print("Playing the book...")

    # This function is used to pause the book using the VLC media player
    def pause_book(self):
        """Pauses the book using the VLC media player."""
        self.player.pause()
        print("Book paused.")

    # This function is used to get the current time of the book in milliseconds
    def get_time(self):
        """Returns the current playback time of the book in milliseconds."""
        return self.player.get_time()

    # This function is used to get the length of the book in milliseconds
    def get_length(self):
        """Returns the total length of the book in milliseconds."""
        return self.player.get_length()

    # This function is used to skip forward in the book by a certain amount of time in milliseconds
    def skip_forward(self, milliseconds):
        """Skips forward in the book by the specified number of milliseconds."""
        current_time = self.get_time()
        new_time = current_time + milliseconds
        get_length = self.get_length()
        if new_time > get_length:
            new_time = get_length  # Ensure we don't exceed the book length
        self.player.set_time(new_time)
        print(f"Skipped forward {milliseconds} ms.")

