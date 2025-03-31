import logging
from http import HTTPStatus
from flask_login import logout_user
from flask_restx import Namespace, Resource
from flask import request

from app.models.user import UserRole
from app.schemas.user_schema import user_login_response_schema, user_login_schema
from app.utils.auth_utils import auth_required, generate_token, verify_user_basic

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth_ns = Namespace("Auth", description="Authentication management")


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(user_login_schema, validate=True)
    @auth_ns.response(HTTPStatus.OK, "Login successful", user_login_response_schema)
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.response(HTTPStatus.BAD_REQUEST, "Invalid input")
    def post(self) -> tuple[dict, int]:
        """Log in a user and generate an authentication token."""
        data = request.json
        username = data.get("username")
        password = data.get("password")

        user = verify_user_basic(username, password)
        if not user:
            return {"message": "Invalid username or password"}, HTTPStatus.UNAUTHORIZED

        token = generate_token(user)
        return {
            "success": True,
            "token": f"Bearer {token}",
        }, HTTPStatus.OK


@auth_ns.route("/logout")
class Logout(Resource):
    @auth_ns.response(HTTPStatus.OK, "Logout successful")
    @auth_ns.response(HTTPStatus.UNAUTHORIZED, "Unauthorized")
    @auth_ns.doc(security=["basic", "jwt"])
    @auth_required([UserRole.ADMIN])
    def get(self) -> tuple[dict, int]:
        """Log out an admin user (admin only)."""
        logout_user()
        return {"success": True, "message": "Logged out successfully"}, HTTPStatus.OK
