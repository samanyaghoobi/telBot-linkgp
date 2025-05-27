# app/telegram/handlers/exception_handler.py

import traceback
from telebot.types import Message, CallbackQuery
from telebot import TeleBot

from app.utils.notifiers.notify_admin import notify_admins_error
from app.telegram.logger import logger


import traceback
from telebot.types import Message, CallbackQuery
from sqlalchemy.exc import SQLAlchemyError
import pymysql
from telebot import TeleBot

def catch_errors(bot: TeleBot):
    def decorator(func):
        def wrapper(message_or_call, *args, **kwargs):
            try:
                return func(message_or_call, *args, **kwargs)

            except Exception as e:
                chat_id = None
                message_id = None
                user_info = "Unknown"
                user_input = "Unknown"

                try:
                    if isinstance(message_or_call, Message):
                        user = message_or_call.from_user
                        user_info = f"{user.first_name} ({user.id})"
                        user_input = f"Message: {message_or_call.text}"
                        chat_id = message_or_call.chat.id
                        message_id = message_or_call.message_id

                    elif isinstance(message_or_call, CallbackQuery):
                        user = message_or_call.from_user
                        user_info = f"{user.first_name} ({user.id})"
                        user_input = f"Callback: {message_or_call.data}"
                        chat_id = message_or_call.message.chat.id
                        message_id = message_or_call.message.message_id

                    # Optional: delete user message
                    # try:
                    #     if chat_id and message_id:
                    #         bot.delete_message(chat_id=chat_id, message_id=message_id)
                    # except Exception as del_err:
                    #     logger.warning(f"❗️ Couldn't delete message: {del_err}")

                    # Notify user
                    try:
                        bot.send_message(chat_id=chat_id, text="❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
                    except Exception as notify_err:
                        logger.warning(f"❗️ Couldn't notify user: {notify_err}")

                    # Log & notify admin
                    error_trace = traceback.format_exc()
                    notify_admins_error(bot, user_input, e, user_info)

                    if isinstance(e, (SQLAlchemyError, pymysql.MySQLError)):
                        logger.error(f"🛑 Database error from {user_info} | {user_input}")
                    else:
                        logger.error(f"⚠️ Application error from {user_info} | {user_input}")

                    logger.error(error_trace)

                except Exception as internal_err:
                    logger.critical("🔥 INTERNAL ERROR in error handler")
                    logger.critical(traceback.format_exc())

                # Optional: keep or stop execution
                raise e
        return wrapper
    return decorator
