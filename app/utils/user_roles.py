from enum import Enum # Import Enum for user roles

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"