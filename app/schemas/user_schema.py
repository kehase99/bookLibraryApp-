from flask_restx import fields
from app.schemas import api

from flask_restx import reqparse

# Define the schema parser for query parameters
user_query_parser = reqparse.RequestParser()
user_query_parser.add_argument(
    "page", type=int, default=1, help="Page number for pagination"
)
user_query_parser.add_argument(
    "per_page", type=int, default=10, help="Number of items per page"
)
user_query_parser.add_argument(
    "full_name", type=str, required=False, help="Filter by full name"
)
user_query_parser.add_argument(
    "username", type=str, required=False, help="Filter by username"
)
user_query_parser.add_argument(
    "email", type=str, required=False, help="Filter by email"
)
user_query_parser.add_argument(
    "role", type=str, required=False, help="Filter by user role"
)


user_request_model_schema = api.model(
    "UserRequestModel",
    {
        "id": fields.Integer(readonly=True, description="User ID"),
        "full_name": fields.String(required=True, description="Full name"),
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "password": fields.String(required=False, description="Password"),
        "role": fields.String(
            required=True, description="User role (e.g., admin, user)"
        ),
    },
)
user_update_request_model_schema = api.model(
    "UserUpdateRequestModel",
    {
        "full_name": fields.String(required=False, description="Full name"),
        "email": fields.String(required=False, description="Email"),
        "password": fields.String(required=False, description="Password"),
        "role": fields.String(
            required=False, description="User role (e.g., admin, user)"
        ),
    },
)
user_schema = api.model(
    "UserModel",
    {
        "id": fields.Integer(readonly=True, description="User ID"),
        "full_name": fields.String(required=True, description="Full name"),
        "username": fields.String(required=True, description="Username"),
        "email": fields.String(required=True, description="Email"),
        "role": fields.String(
            required=True, description="User role (e.g., admin, user)"
        ),
    },
)

user_response_schema = api.model(
    "UserResponseModel",
    {
        "success": fields.Boolean(),
        "data": fields.Nested(user_schema, skip_none=True),
        "total": fields.Integer(required=False),
        "pages": fields.Integer(required=False),
        "current_page": fields.Integer(required=False),
        "per_page": fields.Integer(required=False),
    },
)
user_login_schema = api.model(
    "UserLoginModel",
    {
        "username": fields.String(required=True, description="Username"),
        "password": fields.String(required=True, description="Password"),
    },
)

user_login_response_schema = api.model(
    "UserLoginResponseModel",
    {
        "success": fields.Boolean(),
        "token": fields.String(),
    },
)
