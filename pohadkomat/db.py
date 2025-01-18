import json
import logging
import os
import sqlite3
from typing import Any

SCHEMA = [
    "CREATE TABLE IF NOT EXISTS media ( id INTEGER PRIMARY KEY, title TEXT, path TEXT )",
    "CREATE UNIQUE INDEX IF NOT EXISTS media_path ON media (path)",
    "CREATE TABLE IF NOT EXISTS state ( key TEXT PRIMARY KEY, value TEXT )",
]


class MediaDB:
    def __init__(self):
        self.conn = sqlite3.connect("/cache/media.db")
        self.c = self.conn.cursor()
        self.ensure_schema()

    def ensure_schema(self):
        for statement in SCHEMA:
            self.c.execute(statement)
        self.conn.commit()

    def get_state(self, key: str) -> Any:
        self.c.execute("SELECT value FROM state WHERE key = ?", (key,))
        row = self.c.fetchone()
        if row is None:
            return None
        return json.loads(row[0])

    def set_state(self, key: str, value: Any):
        self.c.execute(
            "REPLACE INTO state (key, value) VALUES (?, ?)", (key, json.dumps(value))
        )
        self.conn.commit()

    def scan(self, clear: bool = False):
        media_dir = "/media"
        if clear:
            self.c.execute("DELETE FROM media")
            self.c.execute("DELETE FROM state")
            self.conn.commit()

        for root, d, files in sorted(os.walk(media_dir)):
            for file in sorted(files):
                ext = os.path.splitext(file)[1]
                # Ensure we only add audio files
                if ext.lower() not in [".mp3", ".m4a"]:
                    logging.debug(f"Skipping {file}")
                    continue
                # Add media to the database
                path = os.path.join(root, file).removeprefix(media_dir).lstrip("/")
                logging.info(f"Adding file: {path}")
                self.c.execute(
                    "INSERT OR IGNORE INTO media (title, path) VALUES (?, ?)",
                    (file, path),
                )
        self.conn.commit()

    def list_media(self) -> None:
        self.c.execute("SELECT id, path FROM media")
        for row in self.c.fetchall():
            logging.info(f"{row[0]:<3} {row[1]}")

    def get_next(self):
        # Get last played index
        idx = self.get_state("current_idx") or 0
        # Select next media
        self.c.execute("SELECT id, title, path FROM media WHERE id > ? LIMIT 1", (idx,))
        row = self.c.fetchone()
        id, title, path = row
        # Update the index
        self.set_state("current_idx", id)
        # Return media path
        logging.info(f"Cued {title}")
        return path
