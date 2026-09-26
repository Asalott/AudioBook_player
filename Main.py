# This is the main python file

# Note: Remove the print statments after testing is done, they are only for debugging purposes
# imports the flask server app into the Main.py
from server import app

HOST = "127.0.0.1"

if __name__ == "__main__":
     app.run(host=HOST, port=5000)