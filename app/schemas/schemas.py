from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class ContactBase(BaseModel):
    """
    Базовая схема контакта с общими полями,
    используемая как основа для создания и обновления контакта.

    Атрибуты:
        first_name (str): Имя контакта.
        last_name (str): Фамилия контакта.
        email (EmailStr): Электронная почта контакта.
        phone (str): Номер телефона.
        birthday (date): Дата рождения.
        extra (Optional[str]): Дополнительная информация (необязательно).
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    extra: Optional[str] = None


class ContactCreate(ContactBase):
    """
    Схема для создания нового контакта.
    Наследует все поля из ContactBase.
    """

    pass


class ContactUpdate(ContactBase):
    """
    Схема для обновления существующего контакта.
    Наследует все поля из ContactBase.
    """

    pass


class ContactOut(ContactBase):
    """
    Схема для вывода данных контакта с дополнительным полем ID.

    Атрибуты:
        id (int): Уникальный идентификатор контакта.
    """

    id: int

    class Config:
        orm_mode = True
