from src.backend.database import Database
from datetime import datetime, timedelta
import pytz

class DayOfWeekRepository:
    def __init__(self, db):
        self.db = db
        self.timezone = pytz.timezone("Europe/Paris")  # CEST



    def get_playtime_by_day_of_week(self, start_days=0, end_days=120):
        # Устанавливаем текущую дату (19 мая 2025, 06:03 AM CEST)
        current_date = datetime(2025, 5, 19, 6, 3, tzinfo=self.timezone)

        # Формируем интервал дат
        start, end = max(start_days, end_days), min(start_days, end_days)
        start_date = current_date - timedelta(days=start)
        end_date = current_date - timedelta(days=end)

        # Запрос: группируем сессии по дням недели и считаем общее время
        query = """
            SELECT 
                EXTRACT(DOW FROM s.start_time AT TIME ZONE 'Europe/Paris') as day_of_week,
                SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration
            FROM activity_sessions s
            WHERE s.end_time IS NOT NULL
            AND s.start_time >= %s
            AND s.start_time <= %s
            GROUP BY EXTRACT(DOW FROM s.start_time AT TIME ZONE 'Europe/Paris')
        """
        self.db.cursor.execute(query, (start_date, end_date))
        results = self.db.cursor.fetchall()

        # Инициализируем массив для хранения времени по дням недели (0 - воскресенье, 1 - понедельник, ..., 6 - суббота)
        playtime_by_day = [0.0] * 7

        # Обрабатываем результаты
        for row in results:
            day_of_week = int(row[0])  # День недели (0-6)
            duration = float(row[1]) / 3600.0  # Длительность в часах
            playtime_by_day[day_of_week] = duration

        return playtime_by_day





'''from src.backend.database import Database
from datetime import datetime, timedelta
import pytz

class DayOfWeekRepository:
    def __init__(self, db):
        self.db = db
        self.timezone = pytz.timezone("Europe/Paris")  # CEST

    def get_playtime_by_day_of_week(self, start_days=0, end_days=120):
        # Устанавливаем текущую дату (19 мая 2025, 05:57 AM CEST)
        current_date = datetime(2025, 5, 19, 5, 57, tzinfo=self.timezone)

        # Формируем интервал дат
        start, end = max(start_days, end_days), min(start_days, end_days)
        start_date = current_date - timedelta(days=start)
        end_date = current_date - timedelta(days=end)

        # Запрос: группируем сессии по дням недели
        query = """
            SELECT 
                EXTRACT(DOW FROM s.start_time AT TIME ZONE 'Europe/Paris') as day_of_week,
                SUM(EXTRACT(EPOCH FROM (end_time - start_time))) as total_duration,
                DATE(s.start_time AT TIME ZONE 'Europe/Paris') as session_date,
                a.alias,
                s.start_time AT TIME ZONE 'Europe/Paris' as start_time,
                EXTRACT(EPOCH FROM (end_time - start_time)) as session_duration
            FROM activity_sessions s
            JOIN apps a ON s.app_id = a.id
            WHERE s.end_time IS NOT NULL
            AND s.start_time >= %s
            AND s.start_time <= %s
            GROUP BY 
                EXTRACT(DOW FROM s.start_time AT TIME ZONE 'Europe/Paris'),
                DATE(s.start_time AT TIME ZONE 'Europe/Paris'),
                a.alias,
                s.start_time,
                EXTRACT(EPOCH FROM (end_time - start_time))
            ORDER BY session_date, start_time
        """
        self.db.cursor.execute(query, (start_date, end_date))
        results = self.db.cursor.fetchall()

        # Инициализируем массив для хранения времени по дням недели (0 - воскресенье, 1 - понедельник, ..., 6 - суббота)
        playtime_by_day = [0.0] * 7
        # Словарь для хранения сессий по дням недели и датам
        sessions_by_day = {i: {} for i in range(7)}  # {day_of_week: {date: [sessions]}}

        # Обрабатываем результаты
        for row in results:
            day_of_week = int(row[0])  # День недели (0-6)
            duration = float(row[1]) / 3600.0  # Длительность в часах
            session_date = row[2].strftime('%d-%m-%Y')  # Дата
            app_name = row[3]  # Название игры
            start_time = row[4].strftime('%H:%M:%S')  # Время начала сессии
            session_duration = float(row[5]) / 3600.0  # Длительность сессии в часах

            # Добавляем длительность к соответствующему дню недели
            playtime_by_day[day_of_week] += duration

            # Сохраняем информацию о сессии
            if session_date not in sessions_by_day[day_of_week]:
                sessions_by_day[day_of_week][session_date] = []
            sessions_by_day[day_of_week][session_date].append(
                f"Game: {app_name}, Start: {start_time}, Duration: {session_duration:.1f}h"
            )

        # Выводим результаты в консоль
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        print("\n=== Playtime by Day of Week ===")
        for i in range(7):
            print(f"{day_names[i]}: {playtime_by_day[i]:.1f} hours")
            print("Details:")
            for date, sessions in sessions_by_day[i].items():
                print(f"  Date: {date}")
                for session in sessions:
                    print(f"    {session}")
            print()

        return playtime_by_day

# Создаём подключение к базе данных и запускаем
if __name__ == "__main__":
    # Подключаемся к базе данных с параметрами из Database
    db = Database(dbname="activitydb", user="postgres", password="pass", host="localhost", port="5432")

    # Создаём экземпляр репозитория
    repo = DayOfWeekRepository(db)

    # Запускаем метод для получения времени по дням недели
    playtime = repo.get_playtime_by_day_of_week(start_days=0, end_days=120)

    # Выводим сводку
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    print("\nSummary of Playtime by Day of Week:")
    for i in range(7):
        print(f"{day_names[i]}: {playtime[i]:.1f} hours")

    # Закрываем соединение с базой
    db.close()'''