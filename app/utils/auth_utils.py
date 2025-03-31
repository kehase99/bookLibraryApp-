import base64
from datetime import timedelta
from functools import wraps
from http import HTTPStatus
import json
import logging
from typing import Any, Optional

from flask import Flask, g, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_login import login_user

from app.models.user import User, UserRole
from app.models import db

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


basic_auth = HTTPBasicAuth()
jwt_auth = JWTManager()


def init_jwt(app: Flask) -> None:
    jwt_auth.init_app(app)


def generate_token(user: User) -> str:
    user_data = json.dumps(user.to_dict())
    expires = timedelta(day=1)
    token = create_access_token(identity=user_data, expires_delta=expires)

    return token


def verify_user_basic(username: str, password: str) -> Optional[User]:
    user = User.query.filter_by(username=username).first()  #  None | {usern....}

    if user and User.check_password(user.password, password):
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }

        return user

    return None


def verify_user_jwt() -> Optional[User]:
    verify_jwt_in_request()

    user_identity = json.loads(get_jwt_identity())
    user_id = user_identity["user_id"]
    user = User.load_user(user_id)

    if user:
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }

        return user

    return None


def get_user_metadata(auth_header: str) -> tuple[str, str]:
    # `Basic dXNlcjpwYXNzd29yZA==` => [ 'Basic', 'dXNlcjpwYXNzd29yZA==']
    base64_credentials_meta = auth_header.split(" ")
    # base64_credentials = dXNlcjpwYXNzd29yZA==`
    base64_credentials = base64_credentials_meta[1]
    # 'dXNlcjpwYXNzd29yZA==' => `'some username':'some hashed password'`
    credentials = base64.b64decode(base64_credentials).decode("utf-8")
    # ['some username', 'some hashed password']
    provided_username, provided_password = credentials.split(":")

    return provided_username, provided_password


def auth_required(allowed_roles: Optional[list[UserRole]] = None):
    def decorator(func: Any):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            auth_header = request.headers.get("Authorization")

            if auth_header and auth_header.startswith("Bearer "):
                user = verify_user_jwt()  # User | None

                if not user:
                    return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

            elif auth_header and auth_header.startswith("Basic "):
                username, password = get_user_metadata(auth_header)
                user = verify_user_basic(username, password)  # User | None

                if not user:
                    return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

            else:
                return {
                    "message": "Authorization header is missing or invalid"
                }, HTTPStatus.UNAUTHORIZED

            # Role-based access control
            if allowed_roles:
                user_role = user.role
                if user_role not in [role for role in allowed_roles]:
                    return {
                        "message": "You do not have permission to access this resource"
                    }, HTTPStatus.FORBIDDEN

            return func(*args, **kwargs)

        return wrapper

    return decorator
