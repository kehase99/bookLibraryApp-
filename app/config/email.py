import os

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
