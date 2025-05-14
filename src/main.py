# src/main.py
import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from src.backend.database import Database
from src.frontend.controller import AppController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Инициализация базы данных
    db = Database(dbname="activitydb", user="postgres", password="pass")

    # Создание контроллера
    controller = AppController(db)

    # Настройка QML
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_path = os.path.join(current_dir, "../ui/main.qml")

    if not os.path.exists(qml_path):
        print(f"Ошибка: файл {qml_path} не найден")
        sys.exit(-1)

    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        print("Ошибка загрузки QML")
        sys.exit(-1)

    sys.exit(app.exec_())