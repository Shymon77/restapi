from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

mail = Mail()
"""
Объект для работы с отправкой почты через Flask-Mail.
"""

limiter = Limiter(key_func=get_remote_address)
"""
Объект для ограничения частоты запросов (rate limiting) с использованием IP-адреса клиента.
"""

cors = CORS()
"""
Объект для настройки CORS (Cross-Origin Resource Sharing) — разрешает/ограничивает доступ с других доменов.
"""
