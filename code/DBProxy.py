import os.path
import sqlite3


class DBProxy:

    def __init__(self, db_name: str):
        self.db_name = db_name
        full_path = os.path.abspath((db_name))
        print("DB will be saved at:", full_path)
        try:
            self.connection = sqlite3.connect(db_name)
            self.connection.execute('''
                                    CREATE TABLE IF NOT EXISTS dados(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL,
                                    score INTEGER NOT NULL,
                                    date TEXT NOT NULL)
                                    ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def save(self, score_dict: dict):
        try:
            self.connection.execute('INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)', score_dict)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Error saving score {e}")

    def retrieve_top10(self) -> list:
        try:
            return self.connection.execute('SELECT * FROM dados ORDER BY score DESC LIMIT 10').fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving scores: {e}")
            return []

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            print(f"Error closing connection: {e}")

