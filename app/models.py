from sqlalchemy import Column, Integer, String, Date
from .database import Base


class Contact(Base):
    """
    Модель контакта пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор контакта (первичный ключ).
        first_name (str): Имя контакта.
        last_name (str): Фамилия контакта.
        email (str): Электронная почта контакта (уникальна).
        phone (str): Номер телефона контакта.
        birthday (date): Дата рождения контакта.
        extra (str, optional): Дополнительная информация о контакте (необязательное поле).
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    extra = Column(String, nullable=True)


from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    """
    Модель пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя (первичный ключ).
        email (str): Электронная почта пользователя (уникальна, обязательна).
        password (str): Хэш пароля пользователя (обязателен).
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
