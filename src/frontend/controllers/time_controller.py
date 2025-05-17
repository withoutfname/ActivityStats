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
        print("TimeController initialized")
