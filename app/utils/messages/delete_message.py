from app.telegram.bot_instance import bot
from datetime import datetime, timedelta
from app.telegram.logger import logger

scheduled_deletions = []


def schedule_message_deletion(chat_id: int, message_id: int, delay: int = 60):
    """
    ثبت پیام برای حذف بعد از تاخیر مشخص شده
    """
    scheduled_deletions.append((datetime.now() + timedelta(seconds=delay), chat_id, message_id))


def delete_scheduled_messages():
    """
    حذف تمام پیام‌هایی که زمان حذفشان گذشته
    """
    now = datetime.now()
    for entry in scheduled_deletions[:]:
        delete_time, chat_id, message_id = entry
        if delete_time <= now:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logger.warning(f"❌ Error deleting message {message_id} in chat {chat_id}: {e}")
            scheduled_deletions.remove(entry)



