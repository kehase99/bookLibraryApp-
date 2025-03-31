import os

from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), "..", os.environ.get("UPLOAD_FOLDER", "uploads")
)
