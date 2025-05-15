from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal, QVariant

class DashboardController(QObject):
    intervalChanged = pyqtSignal()

    def __init__(self, db):
        super().__init__()
        self.db = db
        self._intervalDays = 0  # Default: today
        print("DashboardController initialized")

    @pyqtProperty(float, notify=intervalChanged)
    def totalPlaytime(self):
        try:
            result = self.db.get_total_playtime_by_interval(self._intervalDays)
            print(f"totalPlaytime for {self._intervalDays} days: {result}")
            return float(result) if result is not None else 0.0
        except Exception as e:
            print(f"Error in totalPlaytime: {e}")
            return 0.0

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def topGames(self):
        try:
            result = self.db.get_top_games_by_interval(self._intervalDays, limit=5)
            print(f"topGames for {self._intervalDays} days: {result}")
            games = [[str(name), float(hours)] for name, hours in result]
            return games
        except Exception as e:
            print(f"Error in topGames: {e}")
            return []

    @pyqtProperty(str, constant=True)
    def trackingStartDate(self):
        try:
            result = self.db.get_tracking_start_date()
            print(f"trackingStartDate: {result}")
            return str(result)
        except Exception as e:
            print(f"Error in trackingStartDate: {e}")
            return "Unknown"

    @pyqtProperty(int, constant=True)
    def maxIntervalDays(self):
        try:
            result = self.db.get_max_interval_days()
            print(f"maxIntervalDays: {result}")
            return result
        except Exception as e:
            print(f"Error in maxIntervalDays: {e}")
            return 30

    @pyqtSlot(int)
    def setIntervalDays(self, days):
        if self._intervalDays != days:
            self._intervalDays = days
            print(f"Interval set to {days} days")
            self.intervalChanged.emit()