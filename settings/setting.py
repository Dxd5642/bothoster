import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

from settings.pathes import BASE_DIR



load_dotenv(str(BASE_DIR / ".env"))



DEBUG = bool(os.getenv("DEBUG")) or True
DATABASE_URL = os.getenv("DATABASE_URL")
HOST = os.getenv("HOST") or "0.0.0.0"
PORT = int(os.getenv("PORT")) or 8000


SESSION_TTL = 60 * 60

# ==== REDIS
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv('REDIS_PORT'))
# ====

ALLOWED_ORIGINS = [
    "https://bothoster.com",
    "https://admin.bothoster.com",
]

ALLOWED_HOSTS = [
    "bothoster.com",
    "admin.bothoster.com",
    "api.bothoster.com"
]


# ========= Конфиг для Yandex рассылки =====
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False, 
    MAIL_SSL_TLS=True,    
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)