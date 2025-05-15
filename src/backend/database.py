import psycopg2
from psycopg2 import Error
from decimal import Decimal
from datetime import datetime


class Database:
    def __init__(self, dbname="activitydb", user="postgres", password="pass", host="localhost", port="5432"):
        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Database connection successful")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def get_total_playtime(self):
        """Get total playtime in hours across all sessions"""
        try:
            self.cursor.execute("""
                SELECT SUM(EXTRACT(EPOCH FROM (end_time - start_time))) 
                FROM activity_sessions 
                WHERE end_time IS NOT NULL
            """)
            total_seconds = self.cursor.fetchone()[0]
            print(f"Total seconds: {total_seconds}")
            if total_seconds is None:
                print("No sessions found, returning 0")
                return 0.0
            return float(total_seconds) / 3600.0
        except Error as e:
            print(f"Error fetching playtime: {e}")
            return 0.0

    def get_total_playtime_by_interval(self, days):
        """Get total playtime in hours for the last N days"""
        try:
            self.cursor.execute("""
                SELECT SUM(EXTRACT(EPOCH FROM (end_time - start_time))) 
                FROM activity_sessions 
                WHERE end_time IS NOT NULL
                  AND start_time >= CURRENT_DATE - INTERVAL '%s days'
            """, (days,))
            total_seconds = self.cursor.fetchone()[0]
            print(f"Total seconds for {days} days: {total_seconds}")
            if total_seconds is None:
                print(f"No sessions found for {days} days, returning 0")
                return 0.0
            return float(total_seconds) / 3600.0
        except Error as e:
            print(f"Error fetching playtime for interval: {e}")
            return 0.0

    def get_top_games(self, limit=3):
        """Get top games by playtime"""
        try:
            self.cursor.execute("""
                SELECT 
                    COALESCE(a.alias, a.name) as name,
                    SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time))) / 3600.0
                FROM activity_sessions s
                JOIN apps a ON s.app_id = a.id
                WHERE s.end_time IS NOT NULL
                GROUP BY a.id, a.alias, a.name
                ORDER BY SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time))) DESC
                LIMIT %s
            """, (limit,))
            result = [(row[0], float(row[1])) for row in self.cursor.fetchall()]
            print(f"Top games result: {result}")
            return result
        except Error as e:
            print(f"Error fetching top games: {e}")
            return []

    def get_top_games_by_interval(self, days, limit=None):
        """Get games by playtime for the last N days"""
        try:
            query = """
                SELECT 
                    COALESCE(a.alias, a.name) as name,
                    SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time))) / 3600.0
                FROM activity_sessions s
                JOIN apps a ON s.app_id = a.id
                WHERE s.end_time IS NOT NULL
                  AND start_time >= CURRENT_DATE - INTERVAL '%s days'
                GROUP BY a.id, a.alias, a.name
                ORDER BY SUM(EXTRACT(EPOCH FROM (s.end_time - s.start_time))) DESC
            """
            params = (days,)
            if limit is not None:
                query += " LIMIT %s"
                params = (days, limit)

            self.cursor.execute(query, params)
            result = [(row[0], float(row[1])) for row in self.cursor.fetchall()]
            print(f"Top games for {days} days: {result}")
            return result
        except Error as e:
            print(f"Error fetching top games for interval: {e}")
            return []

    def get_tracking_start_date(self):
        """Get earliest start_time from activity_sessions"""
        try:
            self.cursor.execute("""
                SELECT MIN(start_time)
                FROM activity_sessions
            """)
            start_date = self.cursor.fetchone()[0]
            print(f"Tracking start date: {start_date}")
            return start_date.strftime("%Y-%m-%d") if start_date else "Unknown"
        except Error as e:
            print(f"Error fetching start date: {e}")
            return "Unknown"

    def get_max_interval_days(self):
        """Get number of days from tracking start date to today"""
        try:
            self.cursor.execute("""
                SELECT EXTRACT(DAY FROM (CURRENT_DATE - MIN(start_time)))
                FROM activity_sessions
            """)
            days = self.cursor.fetchone()[0]
            print(f"Max interval days: {days}")
            return int(float(days)) if days is not None else 30
        except Error as e:
            print(f"Error fetching max interval: {e}")
            return 30

    def close(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")