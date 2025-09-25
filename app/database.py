from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
"""
Строка подключения к базе данных, загружается из переменных окружения.
"""

engine = create_engine(DATABASE_URL)
"""
Объект движка SQLAlchemy для подключения к базе данных.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Фабрика сессий SQLAlchemy.
Используется для создания сессий для взаимодействия с базой данных.
"""

Base = declarative_base()
"""
Базовый класс для всех ORM моделей.
Все модели должны наследоваться от этого класса.
"""
