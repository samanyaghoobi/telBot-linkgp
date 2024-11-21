from telebot import TeleBot
from telebot.types import Message
from functions.custom_functions import check_is_admin
from message_and_text.bot_messages import msg_start_command,msg_error_not_admin
from message_and_text.Markups import markup_user_main,markup_main_admin
from bot_functions.user_check import user_check_DB_and_membership


def command_start(bot:TeleBot,msg:Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    
    username=msg.from_user.username
    user_id=msg.from_user.id
    user_check= user_check_DB_and_membership(bot=bot,user_id=user_id,username=username)
    if not user_check:
        return False
    else:
        bot.send_message(chat_id=msg.chat.id,text=msg_start_command,reply_markup=markup_user_main)
####################
def command_admin(bot:TeleBot,msg:Message):
        if check_is_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text="خوش امدی ادمین",reply_markup=markup_main_admin)
        else:
            bot.send_message(chat_id=msg.chat.id,text=msg_error_not_admin,reply_markup=markup_user_main)