import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    WEBHOOK_SECRET: str = os.getenv("WEBHOOK_SECRET")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()