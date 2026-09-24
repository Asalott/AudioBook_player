# This is the main python file

# import
import vlc  # imports python-vlc
import time # imports time

# path to the book
book_path = 'BOOK_PATH_HERE'
print("Loading the book...")

# time values in milliseconds for the audio player to only play the book for a certain amount of time
sixty_minutes = 3600000 # sixty minutes in secounds
forty_minutes = 2400000 # forty minutes in secounds  
thirty_minutes = 1800000 # thirty minutes in secounds
fifteen_minutes = 900000 # fifteen minutes in secounds

# skip values in milliseconds for the audio player to skip forward or backward in the book
skip_10sec = 10000 # ten secounds in milliseconds

# input from the user to control the audio player hoppfully it will be ui in the future
input_play = input(str("input play if you want to play the book:"))
#input_skip_10sec = input(str("input skip 10sec if you want to skip 10 sec of the book:"))
#input_back_10sec = input(str("input back 10sec if you want to go back 10 sec of the book:"))

if input_play == "play":
    # Designates the player
    player = vlc.MediaPlayer(book_path)
    print("Book loaded successfully.")
    
    # plays the book
    player.play()
    print("Playing the book...")
    
    time.sleep(1)  # adds a delay to allow the player to start to get a proper length value
    
    # gets the length of the book in milliseconds
    get_length = player.get_length()
    print(f"Book length: {get_length} ms")
    
    # time.sleep(get_length / 1000)  # plays the book for its entire length
    # Optional: keep the loop running without blocking forever
    while True:
        # gets the current time of the book in milliseconds
        get_time = player.get_time()
        print(f"Current time: {get_time} ms")

        input_pause = input(str("input pause if you want to pause the book:"))
        
        # checks if the current time is greater than or equal to the length of the book
        if get_time >= get_length:
            print("Book finished playing.")
            break

        elif input_pause == "pause":
            player.pause()
            print("Book paused.")
            break  # exit the loop after pausing
        
        time.sleep(1)  # adds a delay to avoid excessive CPU usage
print("Exiting the program.")
