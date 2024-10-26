import redis
import json
import hashlib
import pandas as pd
import logging
import pyarrow as pa
import pyarrow.parquet as pq

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def set(self, key, value, expire=None):
        value = json.dumps(value)
        self.client.set(key, value, ex=expire)

    def get(self, key):
        value = self.client.get(key)
        if value is not None:
            return json.loads(value)
        return None

    def exists(self, key):
        return self.client.exists(key)

    # Helper Functions for Caching
    def get_cache_key(self, query):
        return hashlib.sha256(query.encode()).hexdigest()

    def cache_query(self, query, result, ttl=3600):
        key = self.get_cache_key(query)
        self.set(key, result, ttl)

    def get_cached_query(self, query):
        key = self.get_cache_key(query)
        return self.get(key)

    # Store Query Results as Files
    def save_results_to_file(self, df, filename, format='csv'):
        if format == 'csv':
            df.to_csv(filename, index=False)
        elif format == 'parquet':
            table = pa.Table.from_pandas(df)
            pq.write_table(table, filename)

    # Execute SQL Query with Caching
    logging.basicConfig(level=logging.INFO)

    def execute_query(self, query, conn, cache=True, ttl=3600, format='csv', filename=None):
        try:
            cached_result = self.get_cached_query(query)
            
            if cached_result:
                logging.info(f"Cache hit for query: {query}")
                return pd.read_json(cached_result)

            # Execute query
            df = pd.read_sql(query, conn)

            # Cache the result
            self.cache_query(query, df.to_json(), ttl)
            logging.info(f"Cache stored for query: {query}")

            # Optionally save the result to a file
            if filename:
                self.save_results_to_file(df, filename, format)

            return df
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise

