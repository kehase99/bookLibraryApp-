from flask_restx import Api

api = Api(
    title="BOOK LIBRARY APP",
    version="1.0",
    description="A Book Library App is a software application designed to manage a collection of books.",
    authorizations={
        "basic": {
            "type": "basic",
            "description": "Basic Authentication - Provide `username:password` in Base64.",
        },
        "jwt": {
            "type": "apiKey",  # JWT
            "in": "header",  # find the key in the header
            "name": "Authorization",  # in the header but under the Authorization section
            "description": "JWT Authentication - Use `Bearer <JWT>` in the header.",
        },
    },
)
