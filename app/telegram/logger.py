import logging
from datetime import datetime
from pathlib import Path
import coloredlogs

# Where to store logs: project_root/logs
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR_NAME = "logs"
MAX_LOG_FILES = 7  # keep logs of last 7 bot starts

log_dir = PROJECT_ROOT / LOG_DIR_NAME
log_dir.mkdir(parents=True, exist_ok=True)

# New log file per process start
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = log_dir / f"log_{timestamp}.log"

def clean_old_logs():
    """Keep only the latest MAX_LOG_FILES log files."""
    log_files = sorted(
        [f for f in log_dir.glob("log_*.log") if f.is_file()],
        key=lambda f: f.stat().st_mtime
    )
    while len(log_files) > MAX_LOG_FILES:
        oldest = log_files.pop(0)
        try:
            oldest.unlink()
        except Exception:
            # Ignore failures to delete; continue pruning others
            pass

# Setup main logger
logger = logging.getLogger("link_bot")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# After creating the new log file, prune older ones
clean_old_logs()

# Enable colored logs in terminal
coloredlogs.install(level="DEBUG", logger=logger, fmt="%(asctime)s [%(levelname)s] %(message)s")

# Also log all telebot logs
telebot_logger = logging.getLogger("telebot")
telebot_logger.setLevel(logging.DEBUG)
telebot_logger.handlers.clear()
telebot_logger.addHandler(file_handler)
telebot_logger.addHandler(stream_handler)
telebot_logger.propagate = False


# SQLAlchemy & PyMySQL logs
sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
sqlalchemy_logger.setLevel(logging.WARNING)
sqlalchemy_logger.addHandler(file_handler)
sqlalchemy_logger.addHandler(stream_handler)
sqlalchemy_logger.propagate = False

pymysql_logger = logging.getLogger("pymysql")
pymysql_logger.setLevel(logging.WARNING)
pymysql_logger.addHandler(file_handler)
pymysql_logger.addHandler(stream_handler)
pymysql_logger.propagate = False

logger.info("🔁 Logger initialized successfully.")
