import mysql.connector # type: ignore
from config import * 
from text import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton as InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup as InlineKeyboardMarkup
bot =TeleBot(token = TOKEN)

########################################################################
#check joining button
markup_join=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
markup_join.add(button)
########################################
#check if user is in channels
def check_join(user_id,channels):
    for channel in channels:
        is_member=bot.get_chat_member(chat_id=channel,user_id=user_id)
        if is_member.status in ['left','kicked']:
            return False
        return True

#message for join
def join_msg(chat_id):
     is_member=check_join(user_id=chat_id,channels=channels)
     if is_member is True:
        #   bot.send_message(chat_id,text=joined_text)
          return True
     elif is_member is False:
          bot.send_message(chat_id,text=not_join_text,reply_markup=markup_join)
          return False
            

#callback query for join
@bot.callback_query_handler(func=lambda call:call.data=="proceed")
def proceed (call):
        is_member=join_msg(chat_id=call.message.chat.id,channels=channels)
        if is_member is True:
           bot.send_message(call.message.chat.id,text=joined_text)     
########################################################################
# /start
@bot.message_handler(commands=['start'])
def start(msg):
       is_member=join_msg(chat_id=msg.chat.id)
       if is_member is True:
            try:
                with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        sql= f"INSERT INTO users(userid) VALUES ({msg.from_user.id})"
                        cursor.execute(sql)
                        connection.commit()
                bot.send_message(chat_id=msg.chat.id,text=new_user_text)
            except:
                bot.send_message(chat_id=msg.chat.id,text=old_user_text)
                  
# for making bot running
bot.infinity_polling()  

