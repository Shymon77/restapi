from itsdangerous import URLSafeTimedSerializer
import os
from flask_mail import Message
from app.extensions import mail
from flask import url_for


def generate_confirmation_token(email: str) -> str:
    """
    Генерирует токен подтверждения email с использованием секретного ключа и соли.

    :param email: Email пользователя для генерации токена
    :return: Закодированный токен подтверждения
    """
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token: str, expiration: int = 3600) -> str | bool:
    """
    Проверяет и расшифровывает токен подтверждения email, если он не истёк.

    :param token: Токен для проверки
    :param expiration: Время жизни токена в секундах (по умолчанию 3600 секунд)
    :return: Email, если токен валиден, иначе False
    """
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except:
        return False
    return email


def send_confirmation_email(user_email: str) -> None:
    """
    Формирует и отправляет письмо с ссылкой для подтверждения email пользователя.

    :param user_email: Email адрес получателя
    :return: None
    """
    token = generate_confirmation_token(user_email)
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = f'<p>Підтвердіть email: <a href="{confirm_url}">{confirm_url}</a></p>'
    msg = Message(
        "Підтвердження пошти",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[user_email],
    )
    msg.html = html
    mail.send(msg)
