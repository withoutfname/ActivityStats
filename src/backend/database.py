# src/backend/database.py
import psycopg2
from psycopg2 import Error

class Database:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.connection = None
        self.cursor = None
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor()
            print("Подключение к базе данных успешно")
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def fetch_apps(self):
        try:
            self.cursor.execute("SELECT id, alias FROM apps ORDER BY alias")
            return self.cursor.fetchall()
        except Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")