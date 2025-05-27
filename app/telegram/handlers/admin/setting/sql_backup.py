from app.telegram.schaduled.sql_backup import send_latest_backup_to_channel
from telebot.types import CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.message import get_message

@bot.callback_query_handler(func=lambda call: call.data ==  get_message("btn.admin.get_backup"),is_admin=True)
def manual_backup_download(call :CallbackQuery):
    send_latest_backup_to_channel()
