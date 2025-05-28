from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QCoreApplication
import os
import shutil
import sys

class LibraryController(QObject):
    gamesListChanged = pyqtSignal()

    def __init__(self, stats_service):
        super().__init__()
        self._stats_service = stats_service
        self._games_list = []
        # Базовый путь к проекту для папки resources/app_icons
        self._base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

    @pyqtProperty(list, notify=gamesListChanged)
    def gamesList(self):
        return self._games_list

    @pyqtSlot()
    def fetchGames(self):
        """Обновляет список игр из сервиса."""
        try:
            self._games_list = self._stats_service.get_games_list()
            self.gamesListChanged.emit()
        except Exception as e:
            print(f"Error fetching games: {e}")

    @pyqtSlot(int, str)
    def fetchMetadata(self, app_id, game_name):
        """Запускает парсер для получения метаданных."""
        print(f"Fetching metadata for app_id={app_id}, game_name={game_name}")

    @pyqtSlot(int, str, str, 'QVariant')
    def saveManualMetadata(self, app_id, icon_path, genre, year):
        """Сохраняет метаданные вручную."""
        print(f"Saving manual metadata for app_id={app_id}, icon_path={icon_path}, genre={genre}, year={year}")
        try:
            year = None if year == 0 else year  # Преобразуем 0 в None для базы
            self._stats_service.update_game_metadata(app_id, icon_path, genre, year)
            self.fetchGames()  # Обновляем список игр
        except Exception as e:
            print(f"Error saving metadata: {e}")

    @pyqtSlot(str, str, result=str)
    def copyIcon(self, source_path, app_id):
        """Копирует иконку в папку resources/app_icons с новым именем."""
        try:
            # Извлекаем расширение файла
            extension = os.path.splitext(source_path)[1]
            # Формируем новое имя файла
            new_file_name = f"{app_id}_icon{extension}"
            # Формируем полный путь к папке назначения
            destination_dir = os.path.join(self._base_path, "resources", "app_icons")
            os.makedirs(destination_dir, exist_ok=True)  # Создаём папку, если её нет
            destination_path = os.path.join(destination_dir, new_file_name)
            # Копируем файл
            shutil.copy2(source_path, destination_path)
            print(f"Copied icon from {source_path} to {destination_path}")
            # Возвращаем относительный путь для QML
            return f"resources/app_icons/{new_file_name}"
        except Exception as e:
            print(f"Error copying icon: {e}")
            return ""

    @pyqtSlot()
    def runTest(self):
        """Тестовая функция для проверки копирования иконки и сохранения метаданных."""
        # Тестовые данные
        source_path = "C:/Users/emilm/Downloads/header.jpg"
        app_id = 2
        genres = "Simulation, Sandbox, MMO"
        year = 2024

        # Шаг 1: Копирование иконки
        print("Starting icon copy process...")
        new_icon_path = self.copyIcon(source_path, app_id)
        if new_icon_path:
            print(f"Icon copied successfully: {new_icon_path}")
        else:
            print("Failed to copy icon.")
            return

        # Шаг 2: Сохранение метаданных
        print("Saving metadata...")
        self.saveManualMetadata(app_id, new_icon_path, genres, year)
        print("Metadata save process completed.")

        # Вывод обновлённого списка игр
        print("Updated games list:", self.gamesList)

    # Точка входа для запуска теста
    @staticmethod
    def main():
        from src.backend.database import Database
        from src.backend.services import StatsService

        # Инициализация приложения (нужна для PyQt)
        app = QCoreApplication(sys.argv)

        # Инициализация базы данных
        try:
            db = Database()  # Предполагаем, что Database подключается к твоей базе
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            sys.exit(1)

        # Инициализация StatsService
        stats_service = StatsService(db)

        # Инициализация LibraryController
        controller = LibraryController(stats_service)

        # Запуск теста
        controller.runTest()

        # Завершение приложения
        sys.exit(app.exec_())

if __name__ == "__main__":
    LibraryController.main()