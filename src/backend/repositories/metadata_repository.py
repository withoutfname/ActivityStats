from .base_repository import BaseRepository

class MetadataRepository(BaseRepository):
    def get_tracking_start_date(self):
        query = """
            SELECT MIN(start_time)
            FROM activity_sessions
        """
        start_date = self.execute_query(query, fetch_one=True)
        #print(f"Tracking start date: {start_date}")
        return start_date.strftime("%Y-%m-%d") if start_date else "Unknown"

    def get_max_interval_days(self):
        query = """
            SELECT DATE(CURRENT_DATE) - DATE(MIN(start_time))
            FROM activity_sessions
        """
        days = self.execute_query(query, fetch_one=True)
        #print(f"Max interval days: {days}")
        return int(days) if days is not None else 30