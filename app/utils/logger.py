import logging
import os
from datetime import datetime

LOG_DIR = "logs"
MAX_LOG_FILES = 7

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Generate log file name based on current time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = os.path.join(LOG_DIR, f"log_{timestamp}.log")

# Clean old logs
def clean_old_logs():
    log_files = sorted(
        [f for f in os.listdir(LOG_DIR) if f.startswith("log_") and f.endswith(".log")],
        key=lambda name: os.path.getmtime(os.path.join(LOG_DIR, name))
    )
    while len(log_files) > MAX_LOG_FILES:
        oldest = log_files.pop(0)
        os.remove(os.path.join(LOG_DIR, oldest))

clean_old_logs()

# Setup custom logger
logger = logging.getLogger("link_bot")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Redirect telebot logs to custom logger
telebot_logger = logging.getLogger("telebot")
telebot_logger.setLevel(logging.INFO)
telebot_logger.handlers = logger.handlers
telebot_logger.propagate = False

logger.info("\U0001F501 Logger initialized successfully.")
