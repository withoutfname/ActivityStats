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
        print(f"Fetching metadata for app_id={app_id}, game_name={game_name}")

    @pyqtSlot(int, str, str, 'QVariant')
    def saveManualMetadata(self, app_id, icon_path, genre, year):
        """Сохраняет метаданные вручную."""
        print(f"Saving manual metadata for app_id={app_id}, icon_path={icon_path}, genre={genre}, year={year}")
        year = None if year == 0 else year  # Преобразуем 0 в None для базы
        self._stats_service.update_game_metadata(app_id, icon_path, genre, year)
        self.fetchGames()  # Обновляем список игр