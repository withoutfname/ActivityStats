from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal, QVariant, QDate

class DashboardController(QObject):
    intervalChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self.stats_service = stats_service
        self._intervalDays = 0
        print("DashboardController initialized")

    @pyqtProperty(float, notify=intervalChanged)
    def totalFullPlaytime(self):
        try:
            result = self.stats_service.get_full_total_playtime(start_days=self._intervalDays)

            return float(result) if result is not None else 0.0
        except Exception as e:
            return 0.0

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def topGames(self):
        try:
            result = self.stats_service.get_top_games(start_days=self._intervalDays, limit=8)

            games = [[str(name), float(hours)] for name, hours in result]
            return games
        except Exception as e:
            return []

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def pieChartData(self):
        try:
            games = self.stats_service.get_top_games(start_days=self._intervalDays)
            if not games:
                return [["No Data", 1.0]]

            total_hours = sum(hours for _, hours in games)
            if total_hours == 0:
                return [["No Data", 1.0]]

            games_sorted = sorted(games, key=lambda x: x[1], reverse=True)
            threshold = total_hours * 0.05
            major_games = []
            other_hours = 0

            for name, hours in games_sorted:
                if len(major_games) < 5 or hours >= threshold:
                    major_games.append([str(name), float(hours)])
                else:
                    other_hours += hours

            if other_hours > 0:
                if other_hours < total_hours * 0.05 and len(major_games) > 0:
                    major_games[-1][1] += other_hours
                    major_games[-1][0] += " and others"
                else:
                    major_games.append(["Other", float(other_hours)])

            return major_games if major_games else [["No Data", 1.0]]
        except Exception as e:

            return [["No Data", 1.0]]

    @pyqtProperty(str, constant=True)
    def trackingStartDate(self):
        try:
            result = self.stats_service.get_tracking_start_date()

            return str(result)
        except Exception as e:

            return "Unknown"

    @pyqtProperty(int, constant=True)
    def maxIntervalDays(self):
        try:
            result = self.stats_service.get_max_interval_days()

            return result
        except Exception as e:

            return 30

    @pyqtProperty(str, notify=intervalChanged)
    def intervalStartDate(self):
        if self._intervalDays == 0:
            return QDate.currentDate().toString("yyyy-MM-dd")
        start = QDate.currentDate().addDays(-self._intervalDays)
        return start.toString("yyyy-MM-dd")

    @pyqtSlot(int)
    def setIntervalDays(self, days):
        if self._intervalDays != days:
            self._intervalDays = days
            self.intervalChanged.emit()