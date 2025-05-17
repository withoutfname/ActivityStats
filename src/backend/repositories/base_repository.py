from psycopg2 import Error

class BaseRepository:
    def __init__(self, db):
        self.db = db

    def execute_query(self, query, params=(), fetch_one=False):
        try:
            self.db.cursor.execute(query, params)
            if fetch_one:
                result = self.db.cursor.fetchone()
                return result[0] if result else None
            return self.db.cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return None