import logging
import os
from datetime import datetime
import coloredlogs

LOG_DIR = "logs"
MAX_LOG_FILES = 7

os.makedirs(LOG_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(LOG_DIR, f"log_{timestamp}.log")

def clean_old_logs():
    log_files = sorted(
        [f for f in os.listdir(LOG_DIR) if f.startswith("log_") and f.endswith(".log")],
        key=lambda name: os.path.getmtime(os.path.join(LOG_DIR, name))
    )
    while len(log_files) > MAX_LOG_FILES:
        oldest = log_files.pop(0)
        os.remove(os.path.join(LOG_DIR, oldest))

clean_old_logs()

# Create logger
logger = logging.getLogger("link_bot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add handlers only once
logger.handlers.clear()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Colored logs for console
coloredlogs.install(level="INFO", logger=logger, fmt="%(asctime)s [%(levelname)s] %(message)s")

# Apply logger to telebot as well
telebot_logger = logging.getLogger("telebot")
telebot_logger.setLevel(logging.INFO)
telebot_logger.handlers.clear()
telebot_logger.addHandler(file_handler)
telebot_logger.addHandler(stream_handler)
telebot_logger.propagate = False

logger.info("🔁 Logger initialized successfully.")
