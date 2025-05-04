import logging
from telebot import ExceptionHandler
from database.base import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository

class MyExceptionHandler(ExceptionHandler):
    def handle(self, exception):
        # Log the exception
        logging.exception("Unhandled Exception:", exc_info=exception)

        # Optional: notify admin via Telegram
        try:
            from app.telegram.bot_instance import bot
            with SessionLocal() as db:
                repo = BotSettingRepository(db)
                admin_id = int(repo.get("main_admin", "0"))
            if admin_id:
                bot.send_message(admin_id, f"\u26a0\ufe0f Exception occurred:\n`{str(exception)}`", parse_mode="Markdown")
        except Exception:
            pass  # Avoid crashing inside the exception handler itself

        return True  # Continue polling even after exception
