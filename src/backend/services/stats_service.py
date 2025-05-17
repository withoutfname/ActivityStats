from src.backend.repositories import TimeStatsRepository, MetadataRepository, SessionCountRepository, AppRepository
from datetime import datetime

class StatsService:
    def __init__(self, db):

        self.time_stats_repo = TimeStatsRepository(db)
        self.metadata_repo = MetadataRepository(db)
        self.app_repo = AppRepository
        self.session_count_repo = SessionCountRepository

    def get_full_total_playtime(self, start_days=None, end_days=None):
        total_seconds = self.time_stats_repo.get_full_total_seconds(start_days, end_days)
        return total_seconds / 3600.0

    def get_simp_total_playtime(self, start_days=None, end_days=None):
        total_seconds = self.time_stats_repo.get_simp_total_seconds(start_days, end_days)
        return total_seconds / 3600.0

    def get_top_games(self, start_days=None, end_days=None, limit=None):
        return self.app_repo.get_top_games(start_days, end_days, limit)

    def get_tracking_start_date(self):
        return self.metadata_repo.get_tracking_start_date()

    def get_max_interval_days(self):
        return self.metadata_repo.get_max_interval_days()

    def get_full_session_count(self, start_days=None, end_days=None):
        return self.session_count_repo.get_full_session_count(start_days, end_days)

    def get_simp_session_count(self, start_days=None, end_days=None):
        return self.session_count_repo.get_simp_session_count(start_days, end_days)