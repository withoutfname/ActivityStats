# src/frontend/controller.py
from PyQt5.QtCore import QObject, pyqtProperty, QVariant
from src.backend.database import Database

class AppController(QObject):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._apps = self.db.fetch_apps()

    @pyqtProperty(QVariant, constant=True)
    def apps(self):
        return [[app[0], app[1]] for app in self._apps]  # [id, alias]