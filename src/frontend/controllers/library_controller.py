from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty


class LibraryController(QObject):
    gamesListChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self._stats_service = stats_service
        self._games_list = []

    @pyqtProperty(list, notify=gamesListChanged)
    def gamesList(self):
        return self._games_list

    @pyqtSlot()
    def fetchGames(self):
        """Обновляет список игр из сервиса."""
        self._games_list = self._stats_service.get_games_list()
        self.gamesListChanged.emit()

    @pyqtSlot(int, str)
    def fetchMetadata(self, app_id, game_name):
        """Запускает парсер для получения метаданных."""
        # Здесь будет логика парсинга (пока заглушка)
        print(f"Fetching metadata for app_id={app_id}, game_name={game_name}")
        # В будущем вызовет метод сервиса для парсинга

    @pyqtSlot(int, str, str)
    def saveManualMetadata(self, app_id, icon_path, genre):
        """Сохраняет метаданные вручную."""
        print(f"Saving manual metadata for app_id={app_id}, icon_path={icon_path}, genre={genre}")
        # В будущем вызовет метод сервиса для сохранения'''