import os
import sqlite3

class DBProxy:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), 'DBScore.db')
        self.connection = sqlite3.connect(db_path)
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS dados(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def save(self, name, score, date):
        self.connection.execute(
            'INSERT INTO dados (name, score, date) VALUES (?, ?, ?)',
            (name, score, date)
        )
        self.connection.commit()

    def retrieve_top10(self):
        cursor = self.connection.execute(
            'SELECT name, score, date FROM dados ORDER BY score DESC LIMIT 10'
        )
        return cursor.fetchall()

    def close(self):
        self.connection.close()
