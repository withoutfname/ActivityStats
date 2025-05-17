from .base_repository import BaseRepository

class MaxSessionRepository(BaseRepository):
    def get_max_session(self, start_days, end_days):
        start, end = max(start_days, end_days), min(start_days, end_days)
        query = """
            SELECT 
                start_time,
                end_time,
                EXTRACT(EPOCH FROM (end_time - start_time)) / 3600.0 AS duration,
                COALESCE(a.alias, a.name) AS game
            FROM activity_sessions s
            JOIN apps a ON s.app_id = a.id
            WHERE end_time IS NOT NULL
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
              AND start_time >= CURRENT_DATE - INTERVAL '%s days'
              AND start_time <= CURRENT_DATE - INTERVAL '%s days'
            ORDER BY duration DESC
            LIMIT 1
        """
        row = self.execute_query(query, (start, end), fetch_one=True)
        if row:
            start = row[0].strftime("%Y-%m-%d %H:%M")
            duration = float(row[2])
            game = str(row[3])
            print(f"Max session for range {start_days} to {end_days} days: {duration}h on {start} ({game})")
            return [start, duration, game]
        print(f"No max session found for range {start_days} to {end_days} days")
        return ["N/A", 0.0, "N/A"]

    def get_max_game_session_by_day(self, start_days, end_days):
        start, end = max(start_days, end_days), min(start_days, end_days)
        query = """
            SELECT 
                DATE(start_time) AS game_day,
                COALESCE(a.alias, a.name) AS game,
                SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0 AS total_duration
            FROM activity_sessions s
            JOIN apps a ON s.app_id = a.id
            WHERE end_time IS NOT NULL
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
              AND start_time >= CURRENT_DATE - INTERVAL '%s days'
              AND start_time <= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY DATE(start_time), a.id, a.alias, a.name
            ORDER BY total_duration DESC
            LIMIT 1
        """
        row = self.execute_query(query, (start, end), fetch_one=True)
        if row:
            date = row[0].strftime("%Y-%m-%d")
            game = str(row[1])
            duration = float(row[2])
            print(f"Max game session for range {start_days} to {end_days} days: {duration}h on {date} ({game})")
            return [date, duration, game]
        print(f"No max game session found for range {start_days} to {end_days} days")
        return ["N/A", 0.0, "N/A"]