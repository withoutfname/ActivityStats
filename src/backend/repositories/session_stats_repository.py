from .base_repository import BaseRepository

class SessionStatsRepository(BaseRepository):
    def get_total_seconds(self, start_days=None, end_days=None):
        query = """
            SELECT SUM(EXTRACT(EPOCH FROM (end_time - start_time))) 
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

        total_seconds = self.execute_query(query, params, fetch_one=True)
        #print(f"Total seconds for range {start_days} to {end_days} days: {total_seconds}")
        return float(total_seconds) if total_seconds is not None else 0.0

    def get_session_count(self, start_days=None, end_days=None):
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
        print(f"Session count for range {start_days} to {end_days} days: {count}")
        return int(count) if count is not None else 0