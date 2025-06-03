import os
from glob import glob
from app.telegram.bot_instance import bot
from app.telegram.logger import logger
from config import ADMINS

def send_latest_backup_to_channel():
    backup_dir = "/app/backups/sql"
    sql_files = sorted(glob(os.path.join(backup_dir, "*.sql")), key=os.path.getmtime, reverse=True)
    if not sql_files:
        logger.warning(f"No backup files found in {backup_dir}")
        return False
    sended=False
    latest_backup = sql_files[0]
    for admin_id in ADMINS:
        try:
            with open(latest_backup, "rb") as f:
                bot.send_document(chat_id=admin_id, document=f, caption="📦 آخرین بک‌آپ دیتابیس")
                sended=True
        except Exception as e:
            logger.error(f"❌ Failed to send backup to admin {admin_id}: {e}")
    return True if sended else False