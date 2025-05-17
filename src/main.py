import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from src.backend.database import Database
from src.backend.repositories.app_repository import AppRepository
from src.backend.services.stats_service import StatsService
from src.frontend.controllers import DashboardController, TimeController

if __name__ == "__main__":
    print("Starting application...")
    app = QApplication(sys.argv)
    print("QApplication created")

    # Initialize database
    try:
        db = Database()
        print("Database initialized")
    except Exception as e:
        print(f"Database error: {e}")
        sys.exit(-1)

    # Initialize repositories and service
    app_repo = AppRepository(db)
    stats_service = StatsService(db, app_repo)

    # Create controllers
    try:
        dashboard_controller = DashboardController(stats_service)
        time_controller = TimeController(stats_service)
        print("Controllers created")
    except Exception as e:
        print(f"Controller error: {e}")
        sys.exit(-1)

    # Set up QML engine
    print("Setting up QML engine...")
    engine = QQmlApplicationEngine()

    # Connect error signals
    def handle_qml_error(error):
        print(f"QML Error: {error.toString()}")
        for e in error.errors():
            print(f"  {e.toString()}")

    engine.warnings.connect(handle_qml_error)
    print("QML error handler connected")

    # Set controllers in QML context
    engine.rootContext().setContextProperty("dashboardController", dashboard_controller)
    engine.rootContext().setContextProperty("timeController", time_controller)
    print("Controllers set in QML context")

    # Load QML with absolute path
    print("Loading QML...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    qml_path = os.path.join(current_dir, "../ui/main.qml")
    if not os.path.exists(qml_path):
        print(f"Error: QML file {qml_path} not found")
        sys.exit(-1)

    engine.load(QUrl.fromLocalFile(qml_path))
    print(f"QML file loaded: {qml_path}")

    if not engine.rootObjects():
        print("Error: No root objects loaded")
        sys.exit(-1)

    print("QML loaded successfully")
    sys.exit(app.exec_())