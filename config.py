import os
from dotenv import load_dotenv

load_dotenv(override=True,verbose=True)


def _clean_env_value(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.lower() in {"none", "null"}:
        return None
    return cleaned


def _get_env(*keys: str, default: str | None = None) -> str | None:
    for key in keys:
        val = _clean_env_value(os.getenv(key))
        if val is not None:
            return val
    return default


def _get_int_env(*keys: str, default: int) -> int:
    raw = _get_env(*keys)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


TELEGRAM_API_TOKEN = _get_env("TELEGRAM_API_TOKEN", "BOT_TOKEN")
TELEGRAM_PROXY_URL = _get_env("TELEGRAM_PROXY_URL", default="") or ""
MYSQL_CONFIG = {
    "host": _get_env("MYSQL_HOST", "DB_HOST", default="mysql"),
    "port": _get_int_env("MYSQL_PORT", "DB_PORT", default=3306),
    "user": _get_env("MYSQL_USER", "DB_USER"),
    "password": _get_env("MYSQL_PASSWORD", "DB_PASSWORD"),
    "database": _get_env("MYSQL_DB", "DB_NAME"),
}

ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x.strip()]
# MAIN_CHANNEL_ID = (os.getenv("MAIN_CHANNEL_ID", "@linkGP"))
MAIN_CHANNEL_ID = (os.getenv("MAIN_CHANNEL_ID", "-1002571844991"))
MANDATORY_CHANNELS = [x.strip() for x in os.getenv("MANDATORY_CHANNELS", "-1002571844991").split(",") if x.strip()]

AVAILABLE_HOURS = [
    "00:00", "00:30",
    "01:00", "01:30", 
    "02:00",
    "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "18:30","19:00", "19:30", "20:00", "20:30",
    "21:00", "21:30","22:00", "22:30", "23:00", "23:30"
]
