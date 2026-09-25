# This is the player python file

# Note: Remove the print statments after testing is done, they are only for debugging purposes
from pathlib import Path
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
        get_time = self.player.get_time()
        if get_time == -1:
            print("Error: Unable to get current time. The book may not be playing.")
            return 0
        return get_time

    # This function is used to get the length of the book in milliseconds
    def get_length(self):
        """Returns the total length of the book in milliseconds."""
        get_length = self.player.get_length()
        if get_length == -1:
            print("Error: Unable to get book length. The book may not be playing.")
            return 0
        return get_length

    # This function is used to skip forward in the book by a certain amount of time in milliseconds
    def skip_forward(self, milliseconds):
        """Skips forward in the book by the specified number of milliseconds."""
        current_time = self.get_time()
        new_time = current_time + milliseconds
        get_length = self.get_length()
        if new_time > get_length:
            new_time = get_length  # Ensure we don't exceed the book length
            return new_time
        elif get_length <= 0:
            return 0 # Ensure we don't exceed the book length if the length is unknown or invalid
        self.player.set_time(new_time)
        print(f"Skipped forward {milliseconds} ms.")

    def skip_backward(self, milliseconds):
        """Skips backward in the book by the specified number of milliseconds."""
        current_time = self.get_time()
        new_time = current_time - milliseconds
        get_length = self.get_length()
        if new_time < 0:
            new_time = 0  # Ensure we don't go below 0
            return new_time
        self.player.set_time(new_time)
        print(f"Skipped backward {milliseconds} ms.")

    def get_chapter(self):
        """Returns the current chapter of the book based on the playback time."""
        # Placeholder implementation; actual chapter detection would require additional metadata
        current_time = self.get_time()
        print(f"Current chapter based on time {current_time} ms.")
        return "Chapter information not available."

    def get_cover_art(self):
        """Returns the cover art of the book if available."""
        # Placeholder implementation; actual cover art retrieval would require additional metadata
        print("Cover art retrieval not implemented.")
        return None

    def stop_book(self):
        self.player.stop()
        print("Book stopped.")
