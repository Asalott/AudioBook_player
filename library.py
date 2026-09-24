# The library.py file
from pathlib import Path

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# This function finds all .m4b files in the specified folder and its subfolders.
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

# this function is used to get all the books in the folder and its subfolders and return them as a list of strings
if __name__ == "__main__":
    books = find_books("books")
    if books:
        print("Found the following .m4b files:")
        for book in books:
            print(book)
