from src.backend.repositories import SessionStatsRepository, TimeAnalysisRepository, MaxSessionRepository, MetadataRepository

class StatsService:
    def __init__(self, db, app_repo):
        self.session_stats_repo = SessionStatsRepository(db)
        self.time_analysis_repo = TimeAnalysisRepository(db)
        self.max_session_repo = MaxSessionRepository(db)
        self.metadata_repo = MetadataRepository(db)
        self.app_repo = app_repo

    def get_total_playtime(self, start_days=None, end_days=None):
        total_seconds = self.session_stats_repo.get_total_seconds(start_days, end_days)
        return total_seconds / 3600.0

    def get_average_session(self, start_days, end_days):
        total_hours = self.get_total_playtime(start_days, end_days)
        session_count = self.session_stats_repo.get_session_count(start_days, end_days)
        if session_count == 0:
            print(f"No sessions in range {start_days} to {end_days} days, average is 0")
            return 0.0
        average_hours = total_hours / session_count
        print(f"Average session for range {start_days} to {end_days} days: {average_hours} hours")
        return average_hours

    def get_weekday_playtime(self, start_days, end_days):
        return self.time_analysis_repo.get_weekday_playtime(start_days, end_days)

    def get_daytime_playtime(self, start_days, end_days):
        """Возвращает общее время игры за утро, день, вечер и ночь в часах."""
        return self.time_analysis_repo.get_daytime_playtime(start_days, end_days)

    def get_max_session(self, start_days, end_days):
        return self.max_session_repo.get_max_session(start_days, end_days)

    def get_max_game_session(self, start_days, end_days):
        return self.max_session_repo.get_max_game_session_by_day(start_days, end_days)

    def get_top_games(self, start_days=None, end_days=None, limit=None):
        return self.app_repo.get_top_games(start_days, end_days, limit)

    def get_tracking_start_date(self):
        return self.metadata_repo.get_tracking_start_date()

    def get_max_interval_days(self):
        return self.metadata_repo.get_max_interval_days()

    def get_average_session_by_subintervals(self, start_days, end_days, num_intervals=5):
        """Разделяет интервал на num_intervals частей и возвращает среднее время сессии для каждой части."""
        print(f"Calculating average session for range {start_days} to {end_days} with {num_intervals} intervals")
        if start_days == end_days:
            return [[0, 0.0]] * num_intervals

        start, end = min(start_days, end_days), max(start_days, end_days)
        interval_length = (start - end) / num_intervals
        result = []

        for i in range(num_intervals):
            sub_end = end + i * interval_length
            sub_start = end + (i + 1) * interval_length
            if sub_start > start:
                sub_start = start
            avg_session = self.get_average_session(int(sub_start), int(sub_end))
            result.insert(0, [int(sub_end), avg_session])
            print(f"Average session for subinterval {int(sub_start)} to {int(sub_end)} days: {avg_session}")

        return result

    def get_daily_average_playtime(self, start_days, end_days):
        """Возвращает среднее время игры за день в часах."""
        total_hours = self.get_total_playtime(start_days, end_days)
        days = max(1, abs(start_days - end_days))  # Минимальное значение 1 день
        daily_average = total_hours / days if days > 0 else 0.0
        print(f"Daily average playtime for range {start_days} to {end_days} days: {daily_average} hours")
        return daily_average