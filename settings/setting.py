import os
from pathlib import Path
from dotenv import load_dotenv

from settings.pathes import BASE_DIR



load_dotenv(str(BASE_DIR / ".env"))



DEBUG = bool(os.getenv("DEBUG")) or True
DATABASE_URL = os.getenv("DATABASE_URL")
HOST = os.getenv("HOST") or "0.0.0.0"
PORT = int(os.getenv("PORT")) or 8000

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
