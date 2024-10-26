import sqlite3
import pandas as pd
import os

class Database:
    def __init__(self, db_filename='example.db', parquet_filename='data.parquet'):
        self.db_filename = db_filename
        self.parquet_filename = parquet_filename
        self._check_file()

    def _check_file(self):
        if not os.path.exists(self.parquet_filename):
            raise FileNotFoundError(f"File {self.parquet_filename} does not exist.")

    def initialize_db(self):
        conn = sqlite3.connect(self.db_filename)
        c = conn.cursor()

        # Create a table
        c.execute('''CREATE TABLE IF NOT EXISTS users (id INT, name TEXT, age INT)''')

        # Insert data if the table is empty
        c.execute("SELECT COUNT(*) FROM users")
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO users (id, name, age) VALUES (1, 'Alice', 30)")
            c.execute("INSERT INTO users (id, name, age) VALUES (2, 'Bob', 25)")
        conn.commit()
        conn.close()

    def load_data(self):
        return pd.read_parquet(self.parquet_filename)

    def save_data(self, df):
        df.to_parquet(self.parquet_filename)
