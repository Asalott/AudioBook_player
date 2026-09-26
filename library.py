# The library.py file
from pathlib import Path
from mutagen.mp4 import MP4
import sqlite3 # imports the sqlite3 module to interact with the SQLite database
import re, subprocess, json

# Note: Remove the print statments after testing is done, they are only for debugging purposes

# This function finds all .m4b files in the specified folder and its subfolders.
class BookLibrary: 
    def find_books(self, folder_path):
        """Finds all .m4b files in the specified folder and its subfolders.

        Args:
            folder_path (str): The path to the folder to search for .m4b files.
        """
        # Check if the folder exists and is a directory
        self.folder = Path(folder_path).resolve()
        if not self.folder.is_dir():
            print(f"Folder '{folder_path}' does not exist.")
            return []
        return sorted(str(path) for path in self.folder.rglob("*.m4b") if path.is_file())

    # This function creates a SQLite database to store book information.
    def create_database(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                path TEXT NOT NULL UNIQUE,
                chapters TEXT,
                cover_path TEXT,
                last_position INTEGER DEFAULT 0,
                series TEXT,
                volume INTEGER
            )
        ''')
        for column, coltype in [("last_position", "INTEGER DEFAULT 0"),
                                ("series", "TEXT"),
                                ("volume", "INTEGER")]:
            try:
                self.cursor.execute(f"ALTER TABLE books ADD COLUMN {column} {coltype}")
            except sqlite3.OperationalError:
                pass
        self.conn.commit()

    def extract_cover_art(self, book_path, output_path):
        self.audio = MP4(book_path)
        self.covers = self.audio.tags.get("covr")
        if not self.covers:
            return None
        self.cover_data = self.covers[0]
        with open(output_path, "wb") as f:
            f.write(self.cover_data)
        return str(output_path)

    def clean_title(self, title):
        """Städar en boktitel för visning: tar bort ASIN-koder och konstiga tecken."""
        title = re.sub(r'\[[^\]]*\]', '', title)              # tar bort [B09CVBKH5L] osv
        title = re.sub(r'[^\w\s.,\'!?&:-]', '', title, flags=re.UNICODE)  # tar bort konstiga tecken
        title = re.sub(r'\s+', ' ', title).strip()             # städar mellanslag
        return title


    # This function loads book information into the SQLite database.
    def load_books_into_database(self, db_path, books):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        covers_dir = Path("covers")
        covers_dir.mkdir(exist_ok=True)

        for book_path in books:
            title = self.clean_title(Path(book_path).stem)
            author = self.extract_author(book_path)
            series, volume = self.extract_series_info(book_path, title)

            cover_output = covers_dir / f"{Path(book_path).stem}.jpg"
            cover_path = self.extract_cover_art(book_path, cover_output)
            chapters = self.extract_chapters(book_path)

            self.cursor.execute('''
                INSERT OR IGNORE INTO books (title, author, path, chapters, cover_path, series, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, book_path, json.dumps(chapters), cover_path, series, volume))
        self.conn.commit()

    # This function retrieves all books from the SQLite database.
    def get_books_from_database(self, db_path):
        """Retrieves all books from the SQLite database.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT title, author, path FROM books')
        books = self.cursor.fetchall()
        self.conn.close()
        return books

    def extract_chapters(self, book_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-i", book_path, "-print_format", "json", "-show_chapters", "-loglevel", "error"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True
            )
            data = json.loads(result.stdout)
            chapters = []
            for ch in data.get("chapters", []):
                chapters.append({
                    "title": ch.get("tags", {}).get("title", "Okänt kapitel"),
                    "start": float(ch.get("start_time", 0)),
                    "end": float(ch.get("end_time", 0))
                })
            return chapters
        except Exception as e:
            print(f"Kunde inte extrahera kapitel: {e}")
            return []

    def save_position(self, db_path, book_id, milliseconds):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET last_position = ? WHERE id = ?", (milliseconds, book_id))
        conn.commit()
        conn.close()

    def get_position(self, db_path, book_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT last_position FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0


    def extract_series_info(self, book_path, title):
        try:
            audio = MP4(book_path)
            tags = audio.tags

            # 1. Prefer the "tone" app's dedicated series tags, when present
            tone_series = tags.get("----:com.pilabor.tone:SERIES")
            tone_part = tags.get("----:com.pilabor.tone:PART")
            if tone_series:
                series = bytes(tone_series[0]).decode("utf-8").strip()
                volume = None
                if tone_part:
                    part_str = bytes(tone_part[0]).decode("utf-8").strip()
                    try:
                        volume = int(float(part_str))
                    except ValueError:
                        volume = None
                if series:
                    return series, volume

            # 2. Fall back to the album tag (used by other files, e.g. Tanya/Overlord)
            album = tags.get("\xa9alb")
            track = tags.get("trkn")
            if album:
                raw_series = str(album[0]).strip()
                series, embedded_volume = self._clean_series_name(raw_series)
                volume = (track[0][0] if track and track[0] else None) or embedded_volume
                if series:
                    return series, volume
        except Exception as e:
            print(f"Kunde inte läsa serie-metadata: {e}")

        # 3. Last resort: regex on the title itself
        match = re.match(r'^(.*?),\s*Vol\.?\s*(\d+)', title)
        if match:
            return match.group(1).strip(), int(match.group(2))

        return None, None

    def _clean_series_name(self, raw):
        volume = None
        vol_match = re.search(r',?\s*Vol\.?\s*(\d+)', raw, flags=re.IGNORECASE)
        if vol_match:
            volume = int(vol_match.group(1))
        cleaned = re.sub(r',?\s*Vol\.?\s*\d+', '', raw, flags=re.IGNORECASE)
        cleaned = re.sub(r'\s*\([^)]*\)', '', cleaned)
        cleaned = re.split(r':', cleaned)[0]          # <- ny rad: klipp vid kolon
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned, volume

    def extract_author(self, book_path):
        """Läser författare från filens metadata. Taggen blandar ofta in
        illustratör/översättare (ibland med '- roll', ibland utan), så vi
        filtrerar bort roll-markerade namn och behåller bara det första
        kvarvarande namnet som den faktiska författaren."""
        try:
            audio = MP4(book_path)
            tags = audio.tags

            tone_author = tags.get("----:com.pilabor.tone:ARTIST")
            if tone_author:
                raw = bytes(tone_author[0]).decode("utf-8").strip()
            else:
                artist = tags.get("\xa9ART")
                raw = str(artist[0]).strip() if artist else None

            if raw:
                names = [n.strip() for n in raw.split(",")]
                authors = [n for n in names if " - " not in n]
                if authors:
                    return authors[0]
        except Exception as e:
            print(f"Kunde inte läsa författare: {e}")

        return "Okänd"

    # This function closes the database connection.
    def close_database(self):
        self.conn.close()



