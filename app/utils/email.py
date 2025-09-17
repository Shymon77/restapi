from itsdangerous import URLSafeTimedSerializer
import os


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except:
        return False
    return email


from flask_mail import Message
from app.extensions import mail
from flask import url_for


def send_confirmation_email(user_email):
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
