from .base_repository import BaseRepository

class TimeAnalysisRepository(BaseRepository):
    def get_daytime_range(self, start_days, end_days):
        start, end = max(start_days, end_days), min(start_days, end_days)
        query = """
            SELECT COALESCE(SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0 / 
                   (SELECT COUNT(DISTINCT DATE(start_time)) 
                    FROM activity_sessions 
                    WHERE end_time IS NOT NULL
                      AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
                      AND start_time >= CURRENT_DATE - INTERVAL '%s days'
                      AND start_time <= CURRENT_DATE - INTERVAL '%s days'), 0)
            FROM activity_sessions
            WHERE end_time IS NOT NULL
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
              AND start_time >= CURRENT_DATE - INTERVAL '%s days'
              AND start_time <= CURRENT_DATE - INTERVAL '%s days'
        """
        total_hours = self.execute_query(query, (start, end, start, end), fetch_one=True)
        print(f"Average daytime for range {start_days} to {end_days} days: {total_hours}")
        return float(total_hours) if total_hours is not None else 0.0

    def get_weekday_playtime(self, start_days, end_days):
        start, end = max(start_days, end_days), min(start_days, end_days)
        query = """
            SELECT 
                EXTRACT(DOW FROM start_time) AS weekday,
                SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0
            FROM activity_sessions
            WHERE end_time IS NOT NULL
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
              AND start_time >= CURRENT_DATE - INTERVAL '%s days'
              AND start_time <= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY EXTRACT(DOW FROM start_time)
            ORDER BY weekday
        """
        result = self.execute_query(query, (start, end))
        if result:
            result = [(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][int(row[0])], float(row[1])) for row in result]
            print(f"Weekday playtime for range {start_days} to {end_days} days: {result}")
            return result
        print(f"No weekday playtime data for range {start_days} to {end_days} days")
        return [["Mon", 0.0], ["Tue", 0.0], ["Wed", 0.0], ["Thu", 0.0], ["Fri", 0.0], ["Sat", 0.0], ["Sun", 0.0]]

    def get_daytime_playtime(self, start_days, end_days):
        start, end = max(start_days, end_days), min(start_days, end_days)
        query = """
            SELECT 
                CASE
                    WHEN EXTRACT(HOUR FROM start_time) BETWEEN 6 AND 12 THEN 'Morning'
                    WHEN EXTRACT(HOUR FROM start_time) BETWEEN 12 AND 18 THEN 'Day'
                    WHEN EXTRACT(HOUR FROM start_time) BETWEEN 18 AND 0 THEN 'Evening'
                    ELSE 'Night'
                END AS period,
                SUM(EXTRACT(EPOCH FROM (end_time - start_time))) / 3600.0
            FROM activity_sessions
            WHERE end_time IS NOT NULL
              AND EXTRACT(EPOCH FROM (end_time - start_time)) >= 1800
              AND start_time >= CURRENT_DATE - INTERVAL '%s days'
              AND start_time <= CURRENT_DATE - INTERVAL '%s days'
            GROUP BY period
        """
        raw_result = self.execute_query(query, (start, end))
        print(f"Raw daytime playtime for range {start_days} to {end_days} days: {raw_result}")
        periods = {"Morning": 0.0, "Day": 0.0, "Evening": 0.0, "Night": 0.0}
        if raw_result:
            for period, hours in raw_result:
                periods[period] = float(hours)
        result = [[key, value] for key, value in periods.items()]
        print(f"Daytime playtime for range {start_days} to {end_days} days: {result}")
        return result