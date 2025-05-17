from .base_repository import BaseRepository

class SessionCountRepository(BaseRepository):
    def get_full_session_count(self, start_days=None, end_days=None):
        query = """
            SELECT COUNT(*) 
            FROM activity_sessions 
            WHERE end_time IS NOT NULL
        """
        params = ()
        if start_days is not None and end_days is not None:
            start, end = max(start_days, end_days), min(start_days, end_days)
            query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days' AND start_time <= CURRENT_DATE - INTERVAL '%s days'"
            params = (start, end)
        elif start_days is not None:
            query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days'"
            params = (start_days,)

        count = self.execute_query(query, params, fetch_one=True)
        print(f"Full session count for range {start_days} to {end_days} days: {count}")
        return int(count[0]) if count and count[0] is not None else 0

    def get_simp_session_count(self, start_days=None, end_days=None):
        query = """
            SELECT COUNT(*) 
            FROM activity_sessions 
            WHERE end_time IS NOT NULL 
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
        """
        params = ()
        if start_days is not None and end_days is not None:
            start, end = max(start_days, end_days), min(start_days, end_days)
            query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days' AND start_time <= CURRENT_DATE - INTERVAL '%s days'"
            params = (start, end)
        elif start_days is not None:
            query += " AND start_time >= CURRENT_DATE - INTERVAL '%s days'"
            params = (start_days,)

        count = self.execute_query(query, params, fetch_one=True)
        print(f"Session count (> 30 min) for range {start_days} to {end_days} days: {count}")
        return int(count[0]) if count and count[0] is not None else 0