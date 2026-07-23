from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Developer Landing API")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OWNER_EMAIL = os.getenv("OWNER_EMAIL")

    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")

    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")


settings = Settings()
