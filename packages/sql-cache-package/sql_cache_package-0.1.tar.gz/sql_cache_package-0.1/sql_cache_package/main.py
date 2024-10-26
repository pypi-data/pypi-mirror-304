import sqlite3
from cache import Cache
from database import Database

def main():
    db = Database()
    db.initialize_db()

    conn = sqlite3.connect(db.db_filename)

    cache = Cache()

    # Example: Set a value in cache
    cache.set('key', {'data': 'value'}, expire=10)

    # Example: Get a value from cache
    cached_value = cache.get('key')
    print(f"Cached Value: {cached_value}")

    # Example SQL Query
    query = "SELECT * FROM users"
    df = cache.execute_query(query, conn, cache=True, ttl=600, format='csv', filename='users.csv')
    print(f"DataFrame: {df}")

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()