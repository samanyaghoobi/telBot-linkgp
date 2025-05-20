# app/telegram/handlers/exception_handler.py

from telebot.types import Message, CallbackQuery
from telebot import TeleBot

from app.utils.notify_admin import notify_admins_error




def catch_errors(bot: TeleBot):
    def decorator(func):
        def wrapper(message_or_call, *args, **kwargs):
            try:
                return func(message_or_call, *args, **kwargs)
            except Exception as e:
                # 1. Extract user info
                if isinstance(message_or_call, Message):
                    user = message_or_call.from_user
                    user_info = f"{user.first_name} ({user.id})"
                    text = f"Message: {message_or_call.text}"
                    chat_id = message_or_call.chat.id
                    message_id = message_or_call.message_id
                elif isinstance(message_or_call, CallbackQuery):
                    user = message_or_call.from_user
                    user_info = f"{user.first_name} ({user.id})"
                    text = f"Callback: {message_or_call.data}"
                    chat_id = message_or_call.message.chat.id
                    message_id = message_or_call.message.message_id
                else:
                    user_info = "Unknown"
                    text = "Unknown"
                    chat_id = None
                    message_id = None

                # 2. Delete user message if possible
                if chat_id and message_id:
                    try:
                        # bot.delete_message(chat_id=chat_id, message_id=message_id)
                        bot.send_message(text="delete message",chat_id=chat_id,reply_to_message_id=message_id)
                        print("delete_message")
                    except:
                        pass  # ignore if already deleted or fails

                # 3. Notify user
                try:
                    bot.send_message(chat_id=chat_id, text="❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
                except:
                    pass

                # 4. Notify admin
                notify_admins_error(bot, text, e, user_info)

                raise e  # optional: remove if you don't want to stop execution
        return wrapper
    return decorator
