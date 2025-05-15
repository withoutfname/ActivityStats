from PyQt5.QtCore import QObject, pyqtProperty, QVariant

class DashboardController(QObject):
    def __init__(self, db):
        super().__init__()
        self.db = db
        print("DashboardController initialized")

    @pyqtProperty(float, constant=True)
    def totalPlaytime(self):
        try:
            result = self.db.get_total_playtime()
            print(f"totalPlaytime: {result}")
            if result is None:
                print("Warning: totalPlaytime is None, returning 0.0")
                return 0.0
            return float(result)
        except Exception as e:
            print(f"Error in totalPlaytime: {e}")
            return 0.0

    @pyqtProperty('QVariantList', constant=True)
    def topGames(self):
        try:
            result = self.db.get_top_games(limit=3)
            print(f"topGames raw: {result}")
            games = [[str(name), float(hours)] for name, hours in result]
            print(f"topGames processed: {games}")
            return games
        except Exception as e:
            print(f"Error in topGames: {e}")
            return []