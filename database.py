
# Импортируем необходимые компоненты из библиотеки SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from config import get_db_url
from sqlalchemy import Column, Integer

# Указываем URL для подключения к базе данных SQLite
# В данном случае база данных будет находиться в файле `itproger.db` в текущей директории
SQL_DB_URL = get_db_url()
# Создаем движок (engine) для работы с базой данных
# `create_engine` создает соединение с базой данных
# Параметр `connect_args={"check_same_thread": False}` позволяет использовать соединение в многопоточных приложениях
engine = create_async_engine(SQL_DB_URL,echo=True)

# Создаем фабрику сессий (sessionmaker) для работы с базой данных
# `sessionmaker` создает объекты сессий, которые используются для взаимодействия с базой данных
# Параметры:
# - `autoflush=False` — отключает автоматическую синхронизацию изменений с базой данных
# - `autocommit=False` — отключает автоматическое подтверждение транзакций
# - `bind=engine` — связывает сессии с созданным движком
session_local = async_sessionmaker( bind=engine,expire_on_commit=False)

# Создаем базовый класс для объявления моделей (таблиц) базы данных
# `declarative_base` возвращает базовый класс, от которого наследуются все модели
# Этот класс используется для создания таблиц и работы с ними через ORM
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


