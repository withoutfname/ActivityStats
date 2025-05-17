
C:\Users\emilm\PycharmProjects\ActivityStats\
├── .venv/                  # Виртуальная среда Python
├── src/                    # Основной код приложения
│   ├── backend/            # Логика бэкенда
│   │   ├── database.py     # Подключение к базе данных
│   │   ├── repositories/   # Репозитории для работы с данными
│   │   │   ├── __init__.py
│   │   │   ├── base_repository.py
│   │   │   ├── session_stats_repository.py
│   │   │   ├── time_analysis_repository.py
│   │   │   ├── max_session_repository.py
│   │   │   ├── metadata_repository.py
│   │   │   └── app_repository.py
│   │   ├── services/       # Сервисы для бизнес-логики
│   │   │   ├── __init__.py
│   │   │   └── stats_service.py
│   ├── frontend/           # Логика фронтенда (PyQt/QML)
│   │   ├── controllers/    # Контроллеры
│   │       ├── __init__.py
│   │       ├── dashboard_controller.py
│   │       └── time_controller.py
│   │           
│   ├── ui/                 # QML-файлы для интерфейса
│   │   ├── main.qml        # Главный QML-файл
│   │   └── pages/          # Подкаталог для страниц
│   │       ├── Dashboard.qml
│   │       └── Time.qml    # (если существует)
├── main.py                 # Точка входа в приложение