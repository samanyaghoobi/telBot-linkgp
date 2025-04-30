#* send logs to admins
import logging
from telebot import TeleBot
from configs.auth import ADMIN_ID_LIST
from functions.calender_functions import get_current_datetime
from functions.log_functions import get_last_errors, get_latest_log_file
from message_and_text.markup_text import MSG_ERROR_CAPTION, MSG_NO_ERRORS_FOUND, MSG_NO_LOG_FILE, MSG_RESTART

def startMessageToAdmin(disable_notification:bool,bot:TeleBot,enable:bool=True ):
    if not ADMIN_ID_LIST or not isinstance(ADMIN_ID_LIST, list):
        logging.error("ADMIN_ID_LIST is either empty or not a valid list.")
        return False
    text = f'{MSG_RESTART} \n 🚫{get_current_datetime()}🚫'
    try:
        latest_log_file = get_latest_log_file()
    except Exception as e:
        logging.error(f"Error retrieving latest log file: {e}")
        latest_log_file = None

    for admin in ADMIN_ID_LIST:
        if latest_log_file:
            try:
                last_3_errors = get_last_errors(latest_log_file)
                error_message = "\n".join(last_3_errors) if last_3_errors else MSG_NO_ERRORS_FOUND

                with open(latest_log_file, 'rb') as log_file:
                    bot.send_document(admin, log_file, caption=f"{text}\n{MSG_ERROR_CAPTION} {error_message}",
                                      disable_notification=disable_notification)
                logging.info(f"Sent latest log to admin [{admin}]: {latest_log_file}")
            except FileNotFoundError:
                logging.error(f"Log file not found: {latest_log_file}")
                bot.send_message(chat_id=admin, text=f"{text}\n{MSG_NO_LOG_FILE}", disable_notification=disable_notification)
            except Exception as e:
                logging.error(f"Error while sending log file to admin {admin}: {e}")
        else:
            bot.send_message(chat_id=admin, text=f"{text}\n{MSG_NO_LOG_FILE}", disable_notification=disable_notification)
            logging.warning("No log file found to send.")