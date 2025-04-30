import logging
from telebot import TeleBot,apihelper
from telebot.types import ReplyKeyboardMarkup
from database.db_users import db_user_insert, db_user_is_exist
from message_and_text.bot_messages import msg_error_not_member,msg_error_not_in_db,msg_error_general_error,msg_error_bot_cannot_message_user,msg_error_bot_not_in_channel,msg_error_cannot_message_user,msg_error_unexpected_api_error
from message_and_text.markup_text import text_markup_restart
from configs.auth import CHANNELS_USERNAME, SUPPORT_ID
from functions.custom_functions import makeJoinChannelMarkup
def user_check_DB_and_membership(bot: TeleBot, user_id, username, channels=CHANNELS_USERNAME, admin_id=SUPPORT_ID):
    """
    Checks if the user is a member of required channels and if the user exists in the database.
    Sends appropriate messages to both users and admins, and logs errors.
    """
    try:
        # Step 1: Check if the user is a member of required channels
        for channel in channels:
            try:
                is_member = bot.get_chat_member(chat_id=channel, user_id=user_id)
                if is_member.status in ['left', 'kicked']:
                    # Send message to the user if they are not a member
                    markup = makeJoinChannelMarkup(user_id=user_id)
                    bot.send_message(
                        chat_id=user_id, 
                        text=msg_error_not_member,  # Predefined message variable
                        reply_markup=markup
                    )
                    return False

            except apihelper.ApiTelegramException as e:
                # Handle different API exceptions
                if e.result.status_code == 403:  # Forbidden: Can't access the user
                    logging.warning(f"Bot cannot initiate conversation with user {user_id}. Skipping...")
                    bot.send_message(
                        chat_id=admin_id, 
                        text=msg_error_cannot_message_user.format(user_id=user_id)  # Predefined message variable
                    )
                    bot.send_message(
                        chat_id=user_id, 
                        text=msg_error_bot_cannot_message_user  # Predefined user-facing error message
                    )
                    return False

                elif e.result.status_code == 400:  # Bot not in channel
                    logging.error(f"Bot is not a member of the channel {channel}.")
                    bot.send_message(
                        chat_id=admin_id, 
                        text=msg_error_bot_not_in_channel.format(channel=channel)  # Predefined message variable
                    )
                    return False

                else:  # Unexpected API error
                    logging.error(f"Unexpected API error for user {user_id}: {e}")
                    bot.send_message(
                        chat_id=admin_id, 
                        text=msg_error_unexpected_api_error.format(user_id=user_id, error=e.description)  # Predefined message variable
                    )
                    bot.send_message(
                        chat_id=user_id, 
                        text=msg_error_general_error  # Predefined user-facing general error message
                    )
                    continue

        # Step 2: Check if the user exists in the database
        if not db_user_is_exist(user_id=user_id):
            # Attempt to insert the user into the database
            db_user_insert(userid=user_id, username=username)
            if not db_user_is_exist(user_id=user_id):  # Check again after insertion
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(text_markup_restart)  # Predefined markup for restarting
                bot.send_message(
                    chat_id=user_id, 
                    text=msg_error_not_in_db,  # Predefined message variable
                    reply_markup=markup
                )
                return False

        return True

    except apihelper.ApiTelegramException as e:
        # Handle API exceptions that occur outside the channel loop
        if e.result.status_code == 403:  # Forbidden: Bot can't contact admin
            logging.error(f"Bot cannot contact admin {admin_id}. Please check permissions.")
            bot.send_message(
                chat_id=user_id, 
                text=msg_error_general_error  # Predefined general error message
            )
        else:
            logging.error(f"Unexpected API error: {e}")
            bot.send_message(
                chat_id=user_id, 
                text=msg_error_general_error  # Predefined general error message
            )
        return False

    except Exception as e:
        # Handle general unexpected errors
        logging.error(f"Unexpected error: {e}")
        bot.send_message(
            chat_id=user_id, 
            text=msg_error_general_error  # Predefined general error message
        )
        return False
