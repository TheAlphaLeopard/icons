class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        import sqlite3
        self.connection = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS icons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    url TEXT NOT NULL,
                    image_path TEXT NOT NULL
                )
            ''')

    def insert_icon(self, name, url, image_path):
        with self.connection:
            self.connection.execute('''
                INSERT INTO icons (name, url, image_path) VALUES (?, ?, ?)
            ''', (name, url, image_path))

    def close(self):
        if self.connection:
            self.connection.close()