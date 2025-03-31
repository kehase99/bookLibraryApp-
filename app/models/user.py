from enum import Enum
import logging
import secrets
import string

from flask import Flask
from flask_login import UserMixin

from app.models import db
from werkzeug.security import generate_password_hash, check_password_hash

# Correct the logging level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Enum for User Roles
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "role": self.role.value,
        }

    @staticmethod
    def generate_random_password(length: int = 8) -> str:
        characters = string.ascii_letters + string.digits + string.punctuation
        return "".join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def check_password(password_hash: str, password: str) -> bool:
        return check_password_hash(password_hash, password)

    @staticmethod
    def create_user(
        full_name: str, username: str, email: str, password: str, role: UserRole
    ) -> "User":
        hashed_password = generate_password_hash(password)
        return User(
            full_name=full_name,
            username=username,
            password=hashed_password,
            email=email,
            role=role,
        )

    @staticmethod
    def update_user_as_admin(user: "User", data: dict) -> "User":
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
        if "role" in data:
            data["role"] = UserRole(data["role"])
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "role" in data:
            user.role = data["role"]
        return user

    @staticmethod
    def update_user_as_user(user: "User", data: dict) -> "User":
        if "password" in data:
            data["password"] = generate_password_hash(data["password"])
        if "full_name" in data:
            user.full_name = data["full_name"]
        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        return user

    @staticmethod
    def load_user(user_id: int) -> "User":
        return User.query.get(int(user_id))

    @staticmethod
    def create_initial_users(app):
        """Create initial users if they do not already exist."""
        users = [
            {
                "full_name": "Admin",
                "username": "admin",
                "email": "admin@admin.com",
                "role": UserRole.ADMIN,
                "password": "admin123",
            },
            {
                "full_name": "Alice Johnson",
                "username": "alicej",
                "email": "alice.johnson@example.com",
                "role": UserRole.ADMIN,
                "password": "AliceSecure1!",
            },
            {
                "full_name": "Bob Smith",
                "username": "bobsmith",
                "email": "bob.smith@example.com",
                "role": UserRole.USER,
                "password": "BobStrongPwd2@",
            },
            {
                "full_name": "Charlie Evans",
                "username": "charliee",
                "email": "charlie.evans@example.com",
                "role": UserRole.GUEST,
                "password": "CharlieGuest3#",
            },
            {
                "full_name": "Diana Lopez",
                "username": "dianal",
                "email": "diana.lopez@example.com",
                "role": UserRole.USER,
                "password": "DianaUser4$",
            },
            {
                "full_name": "Ethan Brown",
                "username": "ethanb",
                "email": "ethan.brown@example.com",
                "role": UserRole.ADMIN,
                "password": "EthanAdmin5%",
            },
            {
                "full_name": "Fiona Garcia",
                "username": "fionag",
                "email": "fiona.garcia@example.com",
                "role": UserRole.GUEST,
                "password": "FionaGuest6^",
            },
            {
                "full_name": "George Miller",
                "username": "georgem",
                "email": "george.miller@example.com",
                "role": UserRole.USER,
                "password": "GeorgeUser7&",
            },
            {
                "full_name": "Hannah Wilson",
                "username": "hannahw",
                "email": "hannah.wilson@example.com",
                "role": UserRole.ADMIN,
                "password": "HannahAdmin8*",
            },
            {
                "full_name": "Ian Clark",
                "username": "ianclark",
                "email": "ian.clark@example.com",
                "role": UserRole.USER,
                "password": "IanUser9(",
            },
            {
                "full_name": "Julia Martinez",
                "username": "juliam",
                "email": "julia.martinez@example.com",
                "role": UserRole.GUEST,
                "password": "JuliaGuest0)",
            },
            {
                "full_name": "Kevin Harris",
                "username": "kevinh",
                "email": "kevin.harris@example.com",
                "role": UserRole.USER,
                "password": "KevinPass11!",
            },
            {
                "full_name": "Laura Lewis",
                "username": "laural",
                "email": "laura.lewis@example.com",
                "role": UserRole.ADMIN,
                "password": "LauraSecure12@",
            },
            {
                "full_name": "Michael Young",
                "username": "michaely",
                "email": "michael.young@example.com",
                "role": UserRole.USER,
                "password": "MichaelStrong13#",
            },
            {
                "full_name": "Nina Scott",
                "username": "ninas",
                "email": "nina.scott@example.com",
                "role": UserRole.GUEST,
                "password": "NinaGuest14$",
            },
            {
                "full_name": "Oscar Adams",
                "username": "oscara",
                "email": "oscar.adams@example.com",
                "role": UserRole.USER,
                "password": "OscarPass15%",
            },
            {
                "full_name": "Paula Roberts",
                "username": "paular",
                "email": "paula.roberts@example.com",
                "role": UserRole.ADMIN,
                "password": "PaulaSecure16^",
            },
            {
                "full_name": "Quentin Baker",
                "username": "quentinb",
                "email": "quentin.baker@example.com",
                "role": UserRole.GUEST,
                "password": "QuentinGuest17&",
            },
            {
                "full_name": "Rachel Turner",
                "username": "rachelt",
                "email": "rachel.turner@example.com",
                "role": UserRole.USER,
                "password": "RachelUser18*",
            },
            {
                "full_name": "Samuel Phillips",
                "username": "samuelp",
                "email": "samuel.phillips@example.com",
                "role": UserRole.USER,
                "password": "SamuelSecure19(",
            },
            {
                "full_name": "Tina Watson",
                "username": "tinaw",
                "email": "tina.watson@example.com",
                "role": UserRole.GUEST,
                "password": "TinaGuest20)",
            },
        ]

        with app.app_context():
            for user_data in users:
                existing_user = User.query.filter_by(email=user_data["email"]).first()
                if not existing_user:
                    new_user = User.create_user(
                        full_name=user_data["full_name"],
                        username=user_data["username"],
                        email=user_data["email"],
                        role=user_data["role"],
                        password=user_data["password"],
                    )
                    db.session.add(new_user)
                    db.session.commit()
                    logger.info(f"Added user: {user_data['full_name']}")
                else:
                    logger.info(f"user '{user_data['full_name']}' already exists.")
