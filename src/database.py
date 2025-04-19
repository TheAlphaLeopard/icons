import sqlite3


class Database:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS icons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL
                )
            """)

    def insert_icon(self, name, url):
        with self.connection:
            self.connection.execute("""
                INSERT INTO icons (name, url) VALUES (?, ?)
            """, (name, url))

    def close(self):
        self.connection.close()