import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_PROXY_URL = os.getenv("TELEGRAM_PROXY_URL", "")

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DB")
}

ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip()]
MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID", "-1"))
MANDATORY_CHANNELS = [x.strip() for x in os.getenv("MANDATORY_CHANNELS", "").split(",") if x.strip()]
