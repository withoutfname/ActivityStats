from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal, QVariant
from datetime import datetime, timedelta

class TimeController(QObject):
    intervalChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self.stats_service = stats_service
        self._startDays = 0
        self._endDays = 0
        self._maxIntervalDays = self.stats_service.get_max_interval_days()
        self._cache = {}
        print("TimeController initialized")

    def _cache_key(self, prop):
        return f"{prop}_{self._startDays}_{self._endDays}"

    @pyqtProperty(int, notify=intervalChanged)
    def maxIntervalDays(self):
        return self._maxIntervalDays

    @pyqtProperty(int, notify=intervalChanged)
    def startDays(self):
        return self._startDays

    @pyqtProperty(int, notify=intervalChanged)
    def endDays(self):
        return self._endDays

    @pyqtProperty(float, notify=intervalChanged)
    def totalPlaytime(self):
        cache_key = self._cache_key("totalPlaytime")
        if cache_key in self._cache:
            print(f"Returning cached totalPlaytime: {self._cache[cache_key]}")
            return float(self._cache[cache_key])
        try:
            result = self.stats_service.get_total_playtime(self._startDays, self._endDays)
            print(f"Total playtime for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = float(result) if result is not None else 0.0
            return float(self._cache[cache_key])
        except Exception as e:
            print(f"Error in totalPlaytime: {e}")
            return 0.0

    @pyqtProperty(float, notify=intervalChanged)
    def averageSession(self):
        cache_key = self._cache_key("averageSession")
        if cache_key in self._cache:
            print(f"Returning cached averageSession: {self._cache[cache_key]}")
            return float(self._cache[cache_key])
        try:
            result = self.stats_service.get_average_session(self._startDays, self._endDays)
            print(f"Average session for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = float(result) if result is not None else 0.0
            return float(self._cache[cache_key])
        except Exception as e:
            print(f"Error in averageSession: {e}")
            return 0.0

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def weekdayPlaytime(self):
        cache_key = self._cache_key("weekdayPlaytime")
        if cache_key in self._cache:
            return self._cache[cache_key]
        try:
            result = self.stats_service.get_weekday_playtime(self._startDays, self._endDays)
            print(f"Weekday playtime for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error in weekdayPlaytime: {e}")
            return [["Mon", 0.0], ["Tue", 0.0], ["Wed", 0.0], ["Thu", 0.0], ["Fri", 0.0], ["Sat", 0.0], ["Sun", 0.0]]

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def daytimePlaytime(self):
        cache_key = self._cache_key("daytimePlaytime")
        if cache_key in self._cache:
            print(f"Returning cached daytimePlaytime: {self._cache[cache_key]}")
            return self._cache[cache_key]
        try:
            result = self.stats_service.get_daytime_playtime(self._startDays, self._endDays)
            print(f"Daytime playtime for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = result
            print(f"Cached daytimePlaytime: {self._cache[cache_key]}")
            return self._cache[cache_key]
        except Exception as e:
            print(f"Error in daytimePlaytime: {e}")
            return [["Morning", 0.0], ["Day", 0.0], ["Evening", 0.0], ["Night", 0.0]]

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def maxSession(self):
        cache_key = self._cache_key("maxSession")
        if cache_key in self._cache:
            print(f"Returning cached maxSession: {self._cache[cache_key]}")
            return self._cache[cache_key]
        try:
            result = self.stats_service.get_max_session(self._startDays, self._endDays)
            print(f"Max session for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error in maxSession: {e}")
            return ["N/A", 0.0, "N/A"]

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def maxGameSession(self):
        cache_key = self._cache_key("maxGameSession")
        if cache_key in self._cache:
            print(f"Returning cached maxGameSession: {self._cache[cache_key]}")
            return self._cache[cache_key]
        try:
            result = self.stats_service.get_max_game_session(self._startDays, self._endDays)
            print(f"Max game session for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error in maxGameSession: {e}")
            return ["N/A", 0.0, "N/A"]

    @pyqtProperty(int, notify=intervalChanged)
    def gameCount(self):
        cache_key = self._cache_key("gameCount")
        if cache_key in self._cache:
            print(f"Returning cached gameCount: {self._cache[cache_key]}")
            return self._cache[cache_key]
        try:
            games = self.stats_service.get_top_games(self._startDays, self._endDays)
            count = len(games)
            print(f"Game count for range {self._startDays} to {self._endDays} days: {count}")
            self._cache[cache_key] = int(count)
            return self._cache[cache_key]
        except Exception as e:
            print(f"Error in gameCount: {e}")
            return 0

    @pyqtProperty(str, notify=intervalChanged)
    def startDate(self):
        try:
            date = (datetime.now() - timedelta(days=self._startDays)).strftime("%Y-%m-%d")
            print(f"Start date: {date}")
            return date
        except Exception as e:
            print(f"Error in startDate: {e}")
            return "Unknown"

    @pyqtProperty(str, notify=intervalChanged)
    def endDate(self):
        try:
            date = (datetime.now() - timedelta(days=self._endDays)).strftime("%Y-%m-%d")
            print(f"End date: {date}")
            return date
        except Exception as e:
            print(f"Error in endDate: {e}")
            return "Unknown"

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def averageSessionChartData(self):
        cache_key = self._cache_key("averageSessionChartData")
        if cache_key in self._cache:
            print(f"Using cached averageSessionChartData: {self._cache[cache_key]}")
            return self._cache[cache_key]
        try:
            result = self.stats_service.get_average_session_by_subintervals(self._startDays, self._endDays)
            print(f"Average session chart data calculated: {result}")
            self._cache[cache_key] = result
            return result
        except Exception as e:
            print(f"Error in averageSessionChartData: {e}")
            return [[0, 0.0]] * 5

    @pyqtProperty(float, notify=intervalChanged)
    def dailyAveragePlaytime(self):
        cache_key = self._cache_key("dailyAveragePlaytime")
        if cache_key in self._cache:
            print(f"Returning cached dailyAveragePlaytime: {self._cache[cache_key]}")
            return float(self._cache[cache_key])
        try:
            result = self.stats_service.get_daily_average_playtime(self._startDays, self._endDays)
            print(f"Daily average playtime for range {self._startDays} to {self._endDays} days: {result}")
            self._cache[cache_key] = float(result) if result is not None else 0.0
            return float(self._cache[cache_key])
        except Exception as e:
            print(f"Error in dailyAveragePlaytime: {e}")
            return 0.0

    @pyqtSlot(int, int)
    def setIntervalRange(self, startDays, endDays):
        if self._startDays != startDays or self._endDays != endDays:
            self._startDays = startDays
            self._endDays = endDays
            self._cache.clear()  # Очищаем кэш при изменении диапазона
            print(f"Interval range set to {startDays} to {endDays} days")
            self.intervalChanged.emit()