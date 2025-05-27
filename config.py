import os
from dotenv import load_dotenv

load_dotenv(override=True,verbose=True)


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
# MAIN_CHANNEL_ID = (os.getenv("MAIN_CHANNEL_ID", "@linkGP"))
MAIN_CHANNEL_ID = (os.getenv("MAIN_CHANNEL_ID", "-1002571844991"))
MANDATORY_CHANNELS = [x.strip() for x in os.getenv("MANDATORY_CHANNELS", "").split(",") if x.strip()]

AVAILABLE_HOURS = [
    "00:00", "00:30",
    "01:00", "01:30", 
    "02:00",
    "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "18:30","19:00", "19:30", "20:00", "20:30",
    "21:00", "21:30","22:00", "22:30", "23:00", "23:30"
]