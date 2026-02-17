Стек технологий:
    Python 3.11
    FastAPI
    SQLAlchemy
    Alembic
    PostgreSQL 16
    Docker + Docker Compose
    Pydantic
    Pytest
    Uvicorn ASGI Server

1. Собрать и запустить проект
docker-compose up --build

2. Автоматически применятся все миграции и тесты

3. Зайти по ссылки http://127.0.0.1:8000/docs

4. Запустить Эндпоинт "/api/v1/wallets/create" который создаст и выдаст id кошелька