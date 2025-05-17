from psycopg2 import Error

class AppRepository:
    def __init__(self, db):
        self.db = db

    def get_top_games(self, start_days=None, end_days=None, limit=None):
        try:
            query = """
                SELECT 
                    COALESCE(a.alias, a.name) as name,
                    SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0
                FROM activity_sessions s
                JOIN apps a ON s.app_id = a.id
                WHERE s.end_time IS NOT NULL
            """
            params = ()
            if start_days is not None and end_days is not None:
                start, end = max(start_days, end_days), min(start_days, end_days)
                query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days' AND start_time <= CURRENT_DATE - INTERVAL '%s days'"
                params = (start, end)
            elif start_days is not None:
                query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days'"
                params = (start_days,)

            query += " GROUP BY a.id, a.alias, a.name ORDER BY SUM(EXTRACT(EPOCH FROM (end_time - start_time))) DESC"
            if limit is not None:
                query += " LIMIT %s"
                params = params + (limit,) if params else (limit,)

            self.db.cursor.execute(query, params)
            result = [(row[0], float(row[1])) for row in self.db.cursor.fetchall()]
            #print(f"Top games for range {start_days} to {end_days} days: {result}")
            return result
        except Error as e:
            #print(f"Error fetching top games: {e}")
            return []