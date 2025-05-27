import traceback
from telebot import TeleBot
from config import ADMINS
from app.telegram.logger import logger
from database.repository.bot_setting_repository import BotSettingRepository
from database.session import SessionLocal 

def notify_admins_error(bot: TeleBot, context: str, error: Exception, user_info: str = ""):
    error_trace = traceback.format_exc()
    text = (
        f"🚨 <b>Bot Error</b>\n"
        f"<b>Context:</b> {context}\n"
        f"<b>User:</b> {user_info or 'Unknown'}\n\n"
        f"<pre>{error_trace}</pre>"
    )
    try:
        for admin in ADMINS:
            bot.send_message(chat_id=admin, text=text, parse_mode="HTML")
    except Exception as e:
        logger.warning("⚠️ Failed to notify admin: %s", e)

def notify_admins(bot: TeleBot, msgText: str):
    try:
        for admin in ADMINS:
            bot.send_message(chat_id=admin, text=msgText, parse_mode="HTML")
    except Exception as e:
        logger.warning("⚠️ Failed to notify admin: %s", e)
