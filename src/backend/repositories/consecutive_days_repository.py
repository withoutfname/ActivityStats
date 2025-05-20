from src.backend.database import Database
from datetime import datetime, timedelta
import pytz

class ConsecutiveDaysRepository:
    def __init__(self, db):
        self.db = db
        self.timezone = pytz.timezone("Asia/Yekaterinburg")  # UTC+5 для Уфы/Екатеринбурга

    def get_max_consecutive_days(self, start_days, end_days):
        # Получаем текущую дату и время в заданной таймзоне
        current_date = datetime.now(self.timezone)

        # Формируем интервал дат
        start, end = max(start_days, end_days), min(start_days, end_days)
        start_date = current_date - timedelta(days=start)
        end_date = current_date - timedelta(days=end)

        # Запрос: получаем все дни, когда были игровые сессии
        query = """
            SELECT DISTINCT DATE(s.start_time AT TIME ZONE 'Asia/Yekaterinburg') as play_date
            FROM activity_sessions s
            WHERE s.start_time >= %s
            AND s.start_time <= %s
            ORDER BY play_date
        """
        self.db.cursor.execute(query, (start_date, end_date))
        results = self.db.cursor.fetchall()

        if not results:
            return (0, None, None)

        # Преобразуем даты в список
        play_dates = [row[0] for row in results]

        # Ищем максимальную последовательность
        max_streak = 1
        current_streak = 1
        streak_start = play_dates[0]
        max_streak_start = streak_start
        max_streak_end = streak_start

        for i in range(1, len(play_dates)):
            # Проверяем, является ли текущая дата следующей за предыдущей
            if (play_dates[i] - play_dates[i-1]).days == 1:
                current_streak += 1
            else:
                current_streak = 1
                streak_start = play_dates[i]

            # Обновляем максимальную последовательность, если текущая больше
            if current_streak > max_streak:
                max_streak = current_streak
                max_streak_start = streak_start
                max_streak_end = play_dates[i]

        return (max_streak, max_streak_start, max_streak_end)

'''# Тестовый запуск
if __name__ == "__main__":
    # Подключаемся к базе данных
    db = Database(dbname="activitydb", user="postgres", password="pass", host="localhost", port="5432")

    # Создаём экземпляр репозитория
    repo = ConsecutiveDaysRepository(db)

    # Запускаем метод
    streak, start_date, end_date = repo.get_max_consecutive_days(start_days=0, end_days=120)

    # Выводим результат
    if streak > 0:
        print(f"Max Consecutive Days: {streak} (From: {start_date.strftime('%Y-%m-%d')}, To: {end_date.strftime('%Y-%m-%d')})")
    else:
        print("No gaming sessions found in the interval.")

    # Закрываем соединение
    db.close()'''