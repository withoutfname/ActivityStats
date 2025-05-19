from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from datetime import datetime, timedelta

class TimeController(QObject):
    intervalChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self.stats_service = stats_service
        self._startDays = 0
        self._endDays = 0
        self._currentDate = datetime.today()
        print("TimeController initialized")

    @pyqtProperty(int, notify=intervalChanged)
    def startDays(self):
        return self._startDays

    @pyqtProperty(int, notify=intervalChanged)
    def endDays(self):
        return self._endDays

    @pyqtProperty(float, notify=intervalChanged)
    def avgSessionTime(self):
        try:
            result = self.stats_service.get_avg_interval_playtime(self._startDays, self._endDays)
            print(f"avgSessionTime for range {self._startDays} to {self._endDays} days: {result}")
            return float(result) if result is not None else 0.0
        except Exception as e:
            print(f"Error in avgSessionTime: {e}")
            return 0.0

    @pyqtProperty(str, notify=intervalChanged)
    def startDate(self):
        date = self._currentDate - timedelta(days=self._startDays)
        return date.strftime("%Y-%m-%d")

    @pyqtProperty(str, notify=intervalChanged)
    def endDate(self):
        date = self._currentDate - timedelta(days=self._endDays)
        return date.strftime("%Y-%m-%d")



    @pyqtProperty(int, constant=True)
    def maxIntervalDays(self):
        try:
            result = self.stats_service.get_max_interval_days()
            print(f"maxIntervalDays: {result}")
            return result
        except Exception as e:
            print(f"Error in maxIntervalDays: {e}")
            return 30

    @pyqtSlot(int, int)
    def setIntervalRange(self, startDays, endDays):
        if self._startDays != startDays or self._endDays != endDays:
            self._startDays = startDays
            self._endDays = endDays
            print(f"Interval set to {startDays} to {endDays} days")
            self.intervalChanged.emit()


    @pyqtProperty(float, notify=intervalChanged)
    def avgDayPlaytime(self):
        try:
            result = self.stats_service.get_avg_day_playtime(self._startDays, self._endDays)
            return float(result) if result is not None else 0.0
        except Exception as e:
            print(f"Error in avgDayPlaytime: {e}")
            return 0.0

    @pyqtProperty(int, notify=intervalChanged)
    def simpSessionCount(self):
        try:
            result = self.stats_service.get_simp_session_count(self._startDays, self._endDays)
            return int(result) if result is not None else 0
        except Exception as e:
            print(f"Error in simpSessionCount: {e}")
            return 0

    @pyqtProperty(int, notify=intervalChanged)
    def fullTotalPlaytime(self):
        try:
            result = self.stats_service.get_full_total_playtime(self._startDays, self._endDays)
            return int(result) if result is not None else 0
        except Exception as e:
            print(f"Error in simpSessionCount: {e}")
            return 0

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def maxSessionDuration(self):
        try:
            duration, game_name, date = self.stats_service.get_max_session_duration(self._startDays, self._endDays)
            return [float(duration), game_name if game_name else '', date if date else '']
        except Exception as e:
            print(f"Error in maxSessionDuration: {e}")
            return [0.0, '', '']

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def maxDailyGameSession(self):
        try:
            duration, date, game_name, session_count = self.stats_service.get_max_daily_game_session(self._startDays,
                                                                                                     self._endDays)
            return [float(duration), date if date else '', game_name if game_name else '', int(session_count)]
        except Exception as e:
            print(f"Error in maxDailyGameSession: {e}")
            return [0.0, '', '', 0]

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def maxDailyTotalDuration(self):
        try:
            duration, date, game_details = self.stats_service.get_max_daily_total_duration(self._startDays,
                                                                                           self._endDays)
            return [float(duration), date if date else '', game_details if game_details else '']
        except Exception as e:
            print(f"Error in maxDailyTotalDuration: {e}")
            return [0.0, '', '']

    @pyqtProperty('QVariantList', notify=intervalChanged)
    def playtimeByDayOfWeek(self):
        try:
            playtime = self.stats_service.get_playtime_by_day_of_week(self._startDays, self._endDays)
            return [float(x) for x in playtime]
        except Exception as e:
            print(f"Error in playtimeByDayOfWeek: {e}")
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]