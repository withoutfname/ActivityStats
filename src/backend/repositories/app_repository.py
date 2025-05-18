from src.backend.database import Database

class AppRepository:
    def __init__(self, db):
        self.db = db

    def get_top_games(self, start_days=None, end_days=None, limit=None):
        query = """
            SELECT COALESCE(a.alias, a.name) as name,
                   SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0 as hours
            FROM activity_sessions s
            JOIN apps a ON s.app_id = a.id
            WHERE s.end_time IS NOT NULL
        """
        params = []
        if start_days is not None:
            if end_days is not None:
                start, end = max(start_days, end_days), min(start_days, end_days)
                query += " AND start_time >= CURRENT_DATE - INTERVAL %s AND start_time <= CURRENT_DATE - INTERVAL %s"
                params.extend([f"{start} days", f"{end} days"])
            else:
                query += " AND start_time >= CURRENT_DATE - INTERVAL %s"
                params.append(f"{start_days} days")

        query += " GROUP BY a.id, a.alias, a.name ORDER BY hours DESC"
        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)

        print(f"Executing query: {query} with params: {params}")  # Отладка
        self.db.cursor.execute(query, params)
        result = self.db.cursor.fetchall()
        print(f"Raw result from query: {result}")  # Отладка
        result = [(row[0], float(row[1])) for row in result] if result else []
        print(f"Top games for range {start_days} to {end_days} days: {result}")
        return result