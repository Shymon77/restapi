from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Схема для создания нового пользователя.

    Атрибуты:
        email (EmailStr): Электронная почта пользователя.
        password (str): Пароль пользователя (в открытом виде для регистрации).
    """

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """
    Схема для ответа с данными пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        email (EmailStr): Электронная почта пользователя.
    """

    id: int
    email: EmailStr

    class Config:
        orm_mode = True  # Позволяет работать с ORM-моделями напрямую


class Token(BaseModel):
    """
    Схема для представления JWT токенов.

    Атрибуты:
        access_token (str): Токен доступа.
        refresh_token (str): Токен обновления.
        token_type (str): Тип токена (по умолчанию "bearer").
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
