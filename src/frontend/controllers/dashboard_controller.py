from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal, QVariant

class DashboardController(QObject):
    intervalChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self.stats_service = stats_service
        self._intervalDays = 0
        #print("DashboardController initialized")

    @pyqtProperty(float, notify=intervalChanged)
    def totalPlaytime(self):
        try:
            result = self.stats_service.get_total_playtime(start_days=self._intervalDays)
            #print(f"totalPlaytime for {self._intervalDays} days: {result}")
            return float(result) if result is not None else 0.0
        except Exception as e:
            #print(f"Error in totalPlaytime: {e}")
            return 0.0

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def topGames(self):
        try:
            result = self.stats_service.get_top_games(start_days=self._intervalDays, limit=5)
            #print(f"topGames for {self._intervalDays} days: {result}")
            games = [[str(name), float(hours)] for name, hours in result]
            return games
        except Exception as e:
            #print(f"Error in topGames: {e}")
            return []

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def pieChartData(self):
        try:
            games = self.stats_service.get_top_games(start_days=self._intervalDays)
            #print(f"Raw games for pieChartData: {games}")
            if not games:
                #print("No games for pieChartData")
                return [["No Data", 1.0]]

            total_hours = sum(hours for _, hours in games)
            #print(f"Total hours for pieChartData: {total_hours}")
            if total_hours == 0:
                #print("Zero total hours for pieChartData")
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

            #print(f"pieChartData for {self._intervalDays} days: {major_games}")
            return major_games if major_games else [["No Data", 1.0]]
        except Exception as e:
            #print(f"Error in pieChartData: {e}")
            return [["No Data", 1.0]]

    @pyqtProperty(str, constant=True)
    def trackingStartDate(self):
        try:
            result = self.stats_service.get_tracking_start_date()
            #print(f"trackingStartDate: {result}")
            return str(result)
        except Exception as e:
            #print(f"Error in trackingStartDate: {e}")
            return "Unknown"

    @pyqtProperty(int, constant=True)
    def maxIntervalDays(self):
        try:
            result = self.stats_service.get_max_interval_days()
            #print(f"maxIntervalDays: {result}")
            return result
        except Exception as e:
            #print(f"Error in maxIntervalDays: {e}")
            return 30

    @pyqtSlot(int)
    def setIntervalDays(self, days):
        if self._intervalDays != days:  # Исправлено: self._startDays на self._intervalDays
            self._intervalDays = days
            #print(f"Interval set to {days} days")
            self.intervalChanged.emit()