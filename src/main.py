import sys
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from src.backend.database import Database
from src.frontend.controller import DashboardController

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

    # Create controller
    try:
        controller = DashboardController(db)
        print("Controller created")
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

    # Set controller
    engine.rootContext().setContextProperty("controller", controller)
    print("Controller set in QML context")

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