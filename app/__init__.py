from flask import Flask
from app.extensions import mail, limiter, cors
from app.contacts import contacts_bp


def create_app():
    app = Flask(__name__)

    app.config.from_envvar("APP_CONFIG_FILE", silent=True)
    app.config.from_pyfile(".env", silent=True)

    mail.init_app(app)
    limiter.init_app(app)
    cors.init_app(app)

    return app


from app.contacts import contacts_bp

app.register_blueprint(contacts_bp)
