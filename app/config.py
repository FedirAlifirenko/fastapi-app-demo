import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(os.getenv("DEBUG", True))

# Database settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://demo:demo@localhost/demo")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", False)
