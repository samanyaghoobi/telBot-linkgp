import mysql.connector # type: ignore
from config import * 
from text import *
from telebot import TeleBot
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton
from datetime import datetime,timedelta
from convertdate import persian

bot =TeleBot(token = TOKEN)
########################################################################
back_button=InlineKeyboardButton(text="back",callback_data="back")

#markups
markup_join=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
markup_join.add(button)
###
markup_main=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
markup_main.add(free_rime_btn)
markup_main.add(balance_inc_btn)
markup_main.add(user_acc_btn)
markup_main.add(helper_btn)
###

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

def current_date():
     return datetime.now().strftime("%Y-%m-%d")

def cal_date(days):
     return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

def cal_day(days):
    tomorrow_date = datetime.now() + timedelta(days=days)
    tomorrow_weekday = tomorrow_date.weekday()
    tomorrow_persian = days_of_week[tomorrow_weekday]
    return tomorrow_persian

def get_current_datetime():
    # دریافت تاریخ و ساعت لحظه‌ای
    now = datetime.now()
    # تبدیل به رشته با فرمت YYYY-MM-DD HH:MM:SS
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_str

def gregorian_to_jalali(gregorian_date_str):
    """
    Convert Gregorian date from string format 'YYYY-MM-DD' to Jalali (Shamsi) date.
    :param gregorian_date_str: Date in Gregorian calendar in 'YYYY-MM-DD' format
    :return: Date in Jalali calendar in 'YYYY-MM-DD' format
    """
    # Parse the input date string into a datetime object
    gregorian_date = datetime.strptime(gregorian_date_str, '%Y-%m-%d')
    
    # Extract year, month, and day from the datetime object
    year = gregorian_date.year
    month = gregorian_date.month
    day = gregorian_date.day
    
    # Convert Gregorian date to Jalali date
    jalali_date = persian.from_gregorian(year, month, day)
    
    # Format Jalali date into 'YYYY-MM-DD' string
    jalali_date_str = f"{jalali_date[2]}-{jalali_date[1]:02d}-{jalali_date[0]:02d}"
    
    return jalali_date_str

def make_timing_of_day(result):
    text=f"""اخرین بروز رسانی : {get_current_datetime()}
طرح یک
13:00=>{result[1]}
14:00=>{result[2]}
15:00=>{result[3]}
16:00=>{result[4]}
17:00=>{result[5]}
-------------------
طرح دو 
18:00=>{result[6]}
18:30=>{result[7]}
19:00=>{result[8]}
19:30=>{result[9]}
20:00=>{result[10]}
20:30=>{result[11]}
21:00=>{result[12]}
21:30=>{result[13]}
22:00=>{result[14]}
22:30=>{result[15]}
23:00=>{result[16]}
23:30=>{result[17]}
00:00=>{result[18]}
00:30=>{result[19]}
01:00=>{result[20]}
01:30=>{result[21]}
-------------------
پست ویژه
02:00=>{result[22]}
"""
    return text
########################################
#callback query for join
@bot.callback_query_handler(func=lambda call:call.data=="proceed")
def proceed (call):
        is_member=join_msg(chat_id=call.message.chat.id)
        if is_member is True:
           bot.send_message(call.message.chat.id,text=joined_text,reply_markup=markup_main)     
########################################################################
def get_user_balance(user):
    sql= f"SELECT balance from users where userid = {user}"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
               cursor.execute(sql)
               result =cursor.fetchone()
    return result
     
########################################################################
# /start
@bot.message_handler(commands=['start'])
def start(msg):
       is_member=join_msg(chat_id=msg.chat.id)
       if msg.from_user.id == admin_id:
            bot.send_message(chat_id=msg.chat.id,text="خوش امدی ادمین",reply_markup=markup_main)
       elif is_member is True:
            try:
                with mysql.connector.connect(**DB_CONFIG) as connection:
                    with connection.cursor()  as cursor:
                        sql= f"INSERT INTO users(userid) VALUES ({msg.from_user.id})"
                        cursor.execute(sql)
                        connection.commit()
                bot.send_message(chat_id=msg.chat.id,text=new_user_text,reply_markup=markup_main)
            except:
                bot.send_message(chat_id=msg.chat.id,text=old_user_text,reply_markup=markup_main)
########################################################################
#user account
@bot.message_handler(func=lambda m:m.text == user_acc_btn)
def account(msg):
    #  bot.send_message(msg.chat.id,text="hi")
     balance= get_user_balance(msg.from_user.id)
     bot.send_message(msg.chat.id,text=f""""اطلاعات حساب کاربری شما :
نام کاربری : <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.first_name}</a>
شناسه کاربری :<code>{msg.from_user.id}</code>
موجودی : {balance[0]}
""",parse_mode="HTML")
########################################################################
#user account
@bot.message_handler(func=lambda m:m.text == balance_inc_btn)
def account(msg):
    # bot.send_message(chat_id=admin_id,text=f"new user , msg :{msg}")today = datetime.now().strftime("%Y-%m-%d")
    text=cal_date(2)
    bot.send_message(chat_id=msg.chat.id,text=text)
     
########################################################################
#free time
@bot.message_handler(func=lambda m:m.text == free_rime_btn)
def account(msg):
    markup_free_time=InlineKeyboardMarkup(row_width=2) 
    for i in range(7):
        batten_test=InlineKeyboardButton(text=f"{cal_day(i)} : {gregorian_to_jalali(cal_date(i))}",callback_data=f"time_btn_{i}")
        markup_free_time.add(batten_test)

    markup_free_time.add(back_button)
    # text =f"امروز {cal_day(0)} : {gregorian_to_jalali(cal_date(0))} \n میتوانین از لیست زیر روز مورد نظر را انتخاب کنین تا لیست ساعت های خالی آن روز برای شما ارسال شود"
    text=f"از لیست زیر میتوانید روز مورد نظر را برای دریافت ساعت های خالی انتخاب کنید \n امروز {cal_day(0)} : {gregorian_to_jalali(cal_date(0))} "
    bot.send_message(chat_id=msg.chat.id,text=text,reply_markup=markup_free_time)


 # هندلر برای فشردن دکمه‌های شیشه‌ای
@bot.callback_query_handler(func=lambda call: call.data.startswith("time_btn_"))
def handle_button_press(call):
    print(f'-------------------------------------------')
    print(call.data)
    print(f'-------------------------------------------')
    day=int(call.data.split('_')[2])
    bot.answer_callback_query(call.id, f"شما دکمه {call.data.split('_')[2]} را فشار دادید. ")

    #make a query to DB
    try:
        print(f'try ,{day}')
        # print(f'-------------------------------------------')
        sql= f"INSERT INTO channel_timeing(record_date) VALUES ('{cal_date(day)}')"
        with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            connection.commit()
    except:
        print('exept')
        bot.answer_callback_query(call.id, f"error exept in")

    sql= f"SELECT * from channel_timeing where record_date = '{cal_date(day)}'"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()

    # #show result
    bot.send_message(chat_id=call.message.chat.id,text=make_timing_of_day(result))
    
    
########################################################################
@bot.message_handler(func=lambda m:m.text == back_btn)
def account(msg):
     bot.send_message(chat_id=msg.chat.id,text=back_btn_msg,reply_markup=markup_main)

########################################################################

                  
# for making bot running
bot.infinity_polling()  

