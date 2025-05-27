from app.telegram.logger import logger
from app.telegram.schaduled.sql_backup import send_latest_backup_to_channel
from telebot.types import CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.message import get_message

@bot.callback_query_handler(func=lambda call: call.data ==  get_message("btn.admin.get_backup"),is_admin=True)
def manual_backup_download(call :CallbackQuery):
    logger.info("sending backup")
    result = send_latest_backup_to_channel()
    if result :
        bot.delete_message(call.message.chat.id,call.message.id )
    else:
        bot.send_message(call.message.chat.id,text="مشکلی پیش امده است")
