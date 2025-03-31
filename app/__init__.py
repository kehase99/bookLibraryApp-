import logging
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import db
from app.models.books import Book
from app.models.user import User
from app.schemas import api
from app.utils.auth_utils import init_jwt
from app.routes import register_routes
from app.config.database import (
    SQLALCHEMY_DATABASE_URI,
    SECRET_KEY,
    SQLALCHEMY_TRACK_MODIFICATIONS,
)

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    # Allow all localhost and 127.0.0.1 origins
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = SECRET_KEY

    db.init_app(app)

    init_jwt(app)

    Migrate(app, db)

    register_routes(api, app)

    api.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.user_loader(User.load_user)

    User.create_initial_users(app)
    Book.creat_inital_books(app)

    return app
