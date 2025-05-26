# app/telegram/handlers/exception_handler.py

import traceback
from telebot.types import Message, CallbackQuery
from telebot import TeleBot

from app.utils.notifiers.notify_admin import notify_admins_error
from app.utils.logger import logger




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

                    # Delete user message if possible (optional)
                    if chat_id and message_id:
                        try:
                            # bot.delete_message(chat_id=chat_id, message_id=message_id)
                            pass
                        except Exception as del_error:
                            logger.warning(f"Failed to delete message: {del_error}")

                    # Notify user
                    try:
                        bot.send_message(chat_id=chat_id, text="❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
                    except Exception as notify_error:
                        logger.warning(f"Failed to notify user: {notify_error}")

                    # Log and notify admin
                    error_trace = traceback.format_exc()
                    notify_admins_error(bot, user_input, e, user_info)
                    logger.error(f"⚠️ Error from user {user_info}: {user_input}")
                    logger.error(error_trace)

                except Exception as internal_error:
                    logger.critical(f"❌ Error in error handler: {internal_error}")
                    logger.critical(traceback.format_exc())

                # Optional: stop execution or not
                raise e
        return wrapper
    return decorator
