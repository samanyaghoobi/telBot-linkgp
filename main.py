import mysql.connector # type: ignore
import time
import schedule
from datetime import datetime
from config import * 
from text import *
from telebot import TeleBot , custom_filters
from markups import *
from states import *
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from datetime import datetime,timedelta
from convertdate import persian
from db_connections import *
from custom_functions import *

########################################################################
state_storage=StateMemoryStorage()
bot =TeleBot(token = TOKEN,state_storage=state_storage, parse_mode="HTML")

########################################
#restart  msg
def send_startup_message():
     for admin in ADMIN_ID_LIST:
        bot.send_message(admin,text=restart_msg)
          
########################################
#check if user is in channels
def is_member_of(user_id,channels=CHANNELS_ID):
    for channel in channels:
        is_member=bot.get_chat_member(chat_id=channel,user_id=user_id)
        if is_member.status in ['left','kicked']:
            return False
        return True

#message for join
def check_join_msg(chat_id):
     is_member=is_member_of(user_id=chat_id,channels=CHANNELS_ID)
     if is_member is True:
          return True
     elif is_member is False:
          bot.send_message(chat_id,text=not_join_text,reply_markup=markup_join)
          return False
#!
def total_check(user_id):
     is_member = is_member_of(user_id=user_id)
     is_user = get_user(user_id=user_id)
     if is_member:
        if is_user:
            return True
        else:
            bot.send_message(user_id,text=reboot_text,reply_markup=ReplyKeyboardRemove())
            
     else:
        check_join_msg(chat_id=user_id)
     return False

########################################
#callback query for join
@bot.callback_query_handler(func=lambda call:call.data=="proceed")
def proceed (call :CallbackQuery):
        is_member=check_join_msg(chat_id=call.message.chat.id)
        if is_member is True:
          bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=joined_text)
#todo: test section #######################################################################

# # /test
@bot.message_handler(commands=['test'])
def test(msg : Message):
    send_test_msg_to_admin()


def send_scheduled_message():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message_text = f"این یک پیام زمان‌بندی‌شده است که در {current_time} ارسال شده است."
    bot.send_message(ADMIN_ID_LIST[1], message_text)
    print(f"پیام در {current_time} ارسال شد.")
def schedule_jobs():
    schedule.clear()
    for i in range(len(time_of_day)):
        schedule.every().day.at(time_of_day[i]).do(send_scheduled_message)
def schedule_jobs_test():
    schedule.clear()
    for i in range(10):
        schedule.every().day.at(f"01:0{i}").do(send_scheduled_message)

# تابع برای اجرای زمان‌بندی
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
def start_scheduler():
    schedule_jobs_test()  # ثبت وظایف زمان‌بندی‌شده
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # این کار باعث می‌شود Thread با بستن برنامه اصلی بسته شود
    scheduler_thread.start()
#     bot.send_message(msg.chat.id,text="msg to all test")
#     bot.set_state(user_id=msg.from_user.id,state=admin_state.message_to_all,chat_id=msg.chat.id)
    
# @bot.message_handler(state=admin_state.message_to_all)
# def msg(msg : Message):
#     bot.send_message(msg.chat.id,text="ok")
#     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
#         data['msg']=msg.text
#     # bot.send_message(ADMIN_ID_LIST[0],text=f"{data['msg']}")
#     bot.send_message(msg.chat.id,text=f"{data['msg']}")
#     bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

#todo: test section ################################################################
########################################################################
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
       username=msg.from_user.username
       user_id=msg.from_user.id
       is_member=check_join_msg(chat_id=msg.chat.id)#* join 
       if user_id in ADMIN_ID_LIST:
            bot.send_message(chat_id=msg.chat.id,text=admin_welcome_msg,reply_markup=markup_main)
       elif is_member is True:
            result=get_user(user_id=user_id)
            if result is not None:
                bot.send_message(chat_id=msg.chat.id,text=old_user_text,reply_markup=markup_main)
            else:
                result =create_user(userid=user_id,username=username)
                if result is True:
                    bot.send_message(chat_id=msg.chat.id,text=new_user_text,reply_markup=markup_main)
                else:
                    bot.send_message(chat_id=msg.chat.id,text="مشکلی در ثبت نام شما پیش امد",reply_markup=ReplyKeyboardRemove())
#?#######################################################################
#user account
@bot.message_handler(func=lambda m:m.text == user_acc_btn)
def account(msg : Message):
     user_id=msg.from_user.id
     result = total_check(user_id=user_id)
     print(result)
     if result:
            balance= get_user_balance(user_id)
            score=get_user_score(user_id)
            text=make_user_info(user_id=user_id,balance=balance[0],score=score[0],username=msg.from_user.username)
            markup=InlineKeyboardMarkup(row_width=1)
            btn1=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
            #  btn2=InlineKeyboardButton(text=check_reservations_text,callback_data="user_balance_inc")
            markup.add(btn1)
            bot.send_message(user_id,text=text,reply_markup=markup)
#?#######################################################################
#balance inc
@bot.callback_query_handler(func=lambda call: call.data == "user_balance_inc")
def handle_button_press(call : CallbackQuery):
     user_id=call.from_user.id
     result = total_check(user_id=user_id)
     if result:
            markup=InlineKeyboardMarkup()
            buttons =[]
            for index,plan in enumerate(increase_plans,start=0):
                btn=InlineKeyboardButton(text=plan,callback_data=f"plan_{index}")
                buttons.append(btn)
            for btn in buttons:
                markup.add(btn)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=increase_balance_msg,reply_markup=markup)
########################################################################
#balance inc handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("plan_"))
def handle_button_press(call :CallbackQuery):
     user_id=call.from_user.id
     result = total_check(user_id=user_id)
     if result:
        index=int(call.data.split('_')[1])
        text=f"""{increase_balance_msg_final}
    -----------------
    میزان واریزی انتخاب شده برابر {plans[index]} هزار تومان میباشد لطفا واریز نمایید و برای ارسال فیش واریزی از دکمه زیر استفاده کنید """
        markup=InlineKeyboardMarkup()
        btn=InlineKeyboardButton(text="ارسال رسید",callback_data=f"send_receipt_{index}")
        markup.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)
########################################################################
#get pic_receipt
@bot.callback_query_handler(func= lambda m:m.data.startswith("send_receipt_"))
def handle_button_press(call:CallbackQuery):
     user_id=call.from_user.id
     result = total_check(user_id=user_id)
     if result:
        index=int(call.data.split('_')[2])
        text=f"""لطفا عکس رسید خود را ارسال کنید
        {increase_balance_msg_final}
        (مبلِغ واریزی شما {plans[index]} هراز تومان)
        """
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,text=text)
        bot.set_state(user_id=call.message.chat.id,state=user_state.pic_receipt,chat_id=call.message.chat.id)
        with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
            data['plan'] = index


########################################################################
# # send pic for admin 
@bot.message_handler(state=user_state.pic_receipt,content_types=['photo'])
def forward(msg : Message):
    text=f"رسید شما برای ادمین ارسال شد و تا ساعاتی دیگر مورد تایید قرار میگرد \n و پس از ان حساب شما شارژ میشود"
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text="تایید",callback_data="pic_receipt_accept")
    btn2=InlineKeyboardButton(text="رد کردن",callback_data="pic_receipt_deny")
    btn3=InlineKeyboardButton(text="تغییر مبلغ",callback_data="pic_receipt_custom")
    markup.add(btn1,btn2)
    markup.add(btn3)
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        index = int(data.get('plan'))
    forwarded_msg=bot.forward_message(chat_id=ADMIN_ID_LIST[0],from_chat_id=msg.chat.id,message_id=msg.message_id)

    bot.send_message(chat_id=ADMIN_ID_LIST[0],text=f"""id: {msg.from_user.id} ,
username: @{msg.from_user.username} 
balance of user : {get_user_balance(user_id=msg.from_user.id)[0]}
balance increase amount:‌ {plans[index]}  H T
""",reply_markup=markup,reply_to_message_id=forwarded_msg.message_id)
    # bot.send_message(chat_id=ADMIN_ID_LIST[0],text=f"------------------------------",reply_to_message_id=forwarded_msg.message_id)
    bot.send_message(msg.chat.id,text=text)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)


########################################################################
@bot.message_handler(state=user_state.pic_receipt, content_types=['text', 'video', 'document', 'audio', 'sticker', 'voice', 'location', 'contact'])
def handle_non_photo(msg: Message):
    # پیام خطا برای ارسال محتوای غیر از عکس
    bot.send_message(msg.chat.id, "لطفاً فقط یک عکس از رسید خود ارسال کنید.")
#todo : any pic error

#?#######################################################################
#accept btn
@bot.callback_query_handler(func= lambda m:m.data =="pic_receipt_accept")
def admin_deny(call :CallbackQuery):
    user_id=(find_pattern_id(call.message.text))
    info_text=call.message.text
    amount=int(find_pattern_balance_amount(info_text))
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش تایید شد",callback_data="!?!?!?!")
    markup.add(btn)
    try:
        increase_balance(user_id=user_id,increase_amount=amount)
        for index,price in enumerate(price_plans, start=1):
            if amount == price :
                increase_score(user_id=user_id,increase_amount=index)

        new_balance=get_user_balance(user_id=user_id)[0]
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"{info_text} \n -----------\nnew amount: {new_balance} HT",reply_markup=markup)
        bot.send_message(chat_id=user_id,text=f"تراکنش شما تایید و حساب شما شارژ شد  \n برای مشاهده موجودی خود از دکمه '{user_acc_btn}' استفاده کنید") 
    except:
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی در اپدیت موجودی کاربر پیش امده است",reply_markup=markup)
#?#######################################################################
#deny btn
@bot.callback_query_handler(func= lambda m:m.data =="pic_receipt_deny")
def admin_deny(call :CallbackQuery):
    user_id=(find_pattern_id(call.message.text))
    text=call.message.text
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن تراکنش را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)
    bot.send_message(chat_id=user_id,text=f"تراکنش شما از سمت ادمین رد شد \n درصورت نیاز میتوانید با استفاده از دکمه پشتیبانی با ادمین ارتباط برقرار کنید")
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)

    # bot.send_message(chat_id=user_id,,)

#deny msg reason
@bot.callback_query_handler(func= lambda m:m.data.startswith("deny_message_to_"))
def deny_msg(call : CallbackQuery):
    user_id=int(call.data.split('_')[3])
    msg=f"{call.message.text}"
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن تراکنش را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)
    bot.edit_message_text(text=f"{msg} \n------------------- \n علت رد کردن را بنویسید",chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)
    bot.set_state(user_id=call.message.chat.id,state=admin_state.deny_reason,chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id
#send deny reason
@bot.message_handler(state=admin_state.deny_reason)
def deny_reason(msg : Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = int(data.get('user_id'))
    deny_reason_msg=msg.text
    bot.send_message(chat_id=user_id,text=f"علت رد شدن تراکنش شما : \n {deny_reason_msg}")
    bot.send_message(chat_id=msg.from_user.id,text="پیام شما برای کاربر ارسال شد")
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

#?#######################################################################
#support btn
@bot.message_handler(func=lambda m:m.text == support_btn)
def account(msg : Message):
    bot.send_message(chat_id=msg.chat.id,text=support_text)
     
#?#######################################################################
#free time
@bot.message_handler(func=lambda m:m.text == free_rime_btn)
def account(msg : Message):
     user_id=msg.from_user.id
     result = total_check(user_id=user_id)
     if result:
        markup_free_time=InlineKeyboardMarkup(row_width=2) 
        for i in range(7):
            batten_test=InlineKeyboardButton(text=f"{cal_day(i)} : {gregorian_to_jalali(cal_date(i))}",callback_data=f"time_btn_{i}")
            markup_free_time.add(batten_test)

        # markup_free_time.add(back_button)#todo: make back btn
        # text =f"امروز {cal_day(0)} : {gregorian_to_jalali(cal_date(0))} \n می توانید از لیست زیر روز مورد نظر را انتخاب کنین تا لیست ساعت های خالی آن روز برای شما ارسال شود"
        text=f"از لیست زیر می توانید روز مورد نظر را برای دریافت ساعت های خالی انتخاب کنید \n امروز {cal_day(0)} : {gregorian_to_jalali(cal_date(0))} "
        bot.send_message(chat_id=msg.chat.id,text=text,reply_markup=markup_free_time)


########################################################################
#free time handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("time_btn_"))
def handle_button_press(call :CallbackQuery):
     user_id=call.from_user.id
     result_member = total_check(user_id=user_id)
     if result_member:
        day=int(call.data.split('_')[2])
        #todo:check is update
        #todo:except and try reverse
        try:
            sql= f"INSERT INTO channel_timing(record_date) VALUES ('{cal_date(day)}')"
            with mysql.connector.connect(**DB_CONFIG) as connection:
              with connection.cursor()  as cursor:
                cursor.execute(sql)
                connection.commit()
        except:
            bot.answer_callback_query(call.id, f"error except in")

        result =get_day_reserves(day)

        # #show result
        markup_reserve=InlineKeyboardMarkup()
        btn_reserve=InlineKeyboardButton(text=f"رزرو لینک برای تاریخ:{gregorian_to_jalali(cal_date(day))}",callback_data=f"reserve_{day}_{cal_date(day)}")
        markup_reserve.add(btn_reserve)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=make_timing_of_day(result),reply_markup=markup_reserve)
    
################################################
# hour's reserve  handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("reserve_"))
def handle_button_press(call :CallbackQuery):
     user_id=call.from_user.id
     result_member = total_check(user_id=user_id)
     if result_member:
        day_of_week=int(call.data.split('_')[1])
        date=(call.data.split('_')[2])
        result =get_day_reserves(day_of_week)
        markup=InlineKeyboardMarkup(row_width=4)
        buttons=[]
        for i in range (len(time_of_day)):
            if result[(i+1)] == 0:
                btn_day_reserve=InlineKeyboardButton(text=time_of_day[i],callback_data=f"day_{day_of_week}_{i}")
                buttons.append(btn_day_reserve)
        for i in range(0, len(buttons), 3):
            markup.row(*buttons[i:i+3])
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                            text=f" ساعت های خالی برای \n  {days_of_week[day_of_week]} , معادل : {gregorian_to_jalali(date)}",reply_markup=markup)
################################################
# reserve handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def handle_button_press(call:CallbackQuery):
     user_id=call.from_user.id
     result_member = total_check(user_id=user_id)
     if result_member:
     #todo: make sure time is available
     #todo: get link from user, and scheduling it
        day=int(call.data.split('_')[1]) # it is a number in range(0 to 6)
        time=int(call.data.split('_')[2]) # its number , use 'time_of_day[time]'
        user_id=call.from_user.id
        user_balance=int(get_user_balance(user_id=user_id)[0])
        # print(f"{day},{time}")
        price= price_1 if time <5 else price_2 if 5<=time< 21 else price_3
        text=f"{make_reserve_info_text(day=cal_day(day),date=gregorian_to_jalali(cal_date(day)),time=time_of_day[time],price=price)}  \n------------------ \n موجودی حساب شما : {user_balance} هزار تومان"
        markup_balance_low=InlineKeyboardMarkup()
        btn1=InlineKeyboardButton(text="موجودی حساب شما کافی نیست",callback_data=f"send_link_{day}_{time}")
        markup_balance_low.add(btn1)
        markup_ok=InlineKeyboardMarkup()
        btn2=InlineKeyboardButton(text="تایید و ارسال بنر",callback_data=f"get_banner_{day}_{time}")
        btn3=InlineKeyboardButton(text="  ساخت بنر",callback_data=f"make_banner")
        markup_ok.add(btn3,btn2)
        if user_balance >= price:
            markup=markup_ok
        else:
            markup=markup_balance_low
            bot.send_message(chat_id=user_id,text=f"برای شارژ حساب خود از دکمه '{user_acc_btn}' استفاده کنید")
        bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)
#?##############################################
# ساخت بنر
@bot.callback_query_handler(func=lambda call: call.data == "make_banner")
def handle_button_press(call:CallbackQuery):
     user_id=call.from_user.id
     result_member = total_check(user_id=user_id)
     if result_member:
      bot.send_message(chat_id=call.message.chat.id,text="اسم گروه شما چیست؟ \n حداکثر ۲۰ کاراکتر")
      bot.set_state(user_id=call.message.chat.id,state=banner_state.name,chat_id=call.message.chat.id)
     
#################
@bot.message_handler(state =banner_state.name)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['name']=msg.text
     bot.send_message(text="تعداد اعضایگروه شما چند نفر است \n حداکثر ۱۰ کاراکتر",chat_id=msg.chat.id)
     bot.set_state(state=banner_state.member,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.member)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['member']=msg.text
     bot.send_message(text="در یک خط اگر توضیحاتی لازم است برای گروه خود بنویسید \n حداکثر ۳۰ کاراکتر",chat_id=msg.chat.id)
     bot.set_state(state=banner_state.description,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.description)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['description']=msg.text
     bot.send_message(text="لینک خصوصی گروه خود را ارسال کنید",chat_id=msg.chat.id)
     bot.set_state(state=banner_state.link,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.link)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['link']=msg.text
        name=f"{data['name']}"
        member=f"{data['member']}"
        description=f"{data['description']}"
        link=f"{data['link']}"
     print(name,member,description,link)
     banner= make_channel_banner(name=name,members=member,description=description,link=link)

     print(banner)
     bot.send_message(text="بنر شما اماده است",chat_id=msg.chat.id,)
     bot.send_message(text=banner,chat_id=msg.chat.id)
     bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    
#################

#?#######################################################################
@bot.message_handler(func=lambda m:m.text == back_btn)
def account(msg : Message):
     bot.send_message(chat_id=msg.chat.id,text=back_btn_msg,reply_markup=markup_main)

########################################################################
#!#######################################################################
#! admin part  

# /admin
@bot.message_handler(commands=['admin'])
def start(msg : Message):
        if check_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text="خوش امدی ادمین",reply_markup=markup_main_admin)
        else:
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
##########################
#* user list
#todo : paging
@bot.message_handler(func=lambda m:m.text == admin_btn_user_list)
def user_list(msg : Message):
     if not check_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
     users=get_all_users()
     markup = InlineKeyboardMarkup()
     for user in users:
         btn= InlineKeyboardButton(text=f"{user[3]}:{user[0]}",callback_data=f"users_{user[0]}")
         markup.add(btn)
    #  for i in range(1000):
        #  btn=InlineKeyboardButton(text='test',callback_data="test")
        #  markup.add(btn)
     bot.send_message(chat_id=msg.chat.id,text="لیست کاربر ها",reply_markup=markup)
     return True
##########################
#* bot info
@bot.message_handler(func=lambda m:m.text == admin_btn_bot_info)
def user_list(msg : Message):
     if not check_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
     users=get_all_users()
     count_users=len(users)
     text=f"""تعداد کل کاربر های ربات : {count_users}
     سازنده ربات : <a href='tg://user?id={ADMIN_ID_LIST[0]}'>{creator_username}</a>
"""
     bot.send_message(msg.from_user.id,text=text)
##########################
@bot.callback_query_handler(func=lambda call: call.data.startswith("users_"))
def handle_button_press(call :CallbackQuery):
    if not check_admin(call.message.from_user.id):
            bot.send_message(call.message.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    user_id=int(call.data.split('_')[1])
    id=get_user_id(user_id=user_id)
    balance=get_user_balance(user_id=user_id)
    score=get_user_score(user_id=user_id)
    text= make_user_info(username=id[0],user_id=user_id,balance=balance[0],score=score[0])
    markup=InlineKeyboardMarkup(row_width=2)
    btn1=InlineKeyboardButton(text="increase balance",callback_data="increase_balance")
    btn2=InlineKeyboardButton(text="increase score",callback_data="increase_score")
    btn3=InlineKeyboardButton(text="decrease balance",callback_data="decrease_balance")
    btn4=InlineKeyboardButton(text="decrease score",callback_data="decrease_score")
    btn5=InlineKeyboardButton(text="ban user",callback_data="ban_user")
    btn5=InlineKeyboardButton(text="send message",callback_data="send_message")
    markup.add(btn1,btn2,btn3,btn4,btn5)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)
##########################
#?send msg to all
@bot.message_handler(func=lambda m:m.text == admin_btn_send_msg_to_all)
def msg_to_all(msg : Message):
    if not check_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    bot.send_message(chat_id=msg.chat.id,text="پیامی برای ارسال به همه برای من بنویسید")
    bot.set_state(user_id=msg.from_user.id,state=admin_state.message_to_all,chat_id=msg.chat.id)

    
@bot.message_handler(state =admin_state.message_to_all)
def get_message_to_send(msg : Message):
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['msg']=msg.text
    text=f"یک پیام از سمت ادمین :\n <strong> {data['msg']} </strong> "
    users=get_all_users()
    for user in users:
       bot.send_message(chat_id=user[0],text=text, )
    bot.send_message(chat_id=msg.chat.id,text="پیام شما ارسال شد", )
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

##########################
#?check income
@bot.message_handler(func=lambda m:m.text == admin_btn_check_income)
def msg_to_all(msg : Message):
     if not check_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
     markup=InlineKeyboardMarkup(row_width=3)
     buttons = []
     for index,month in enumerate(months, start=1):
          btn=InlineKeyboardButton(text=f"{index}: {month}",callback_data=f"month_{index}")
          buttons.append(btn)
     for i in range(0, len(buttons), 3):
          markup.row(*buttons[i:i+3])
     bot.send_message(msg.chat.id,text=check_income_msg,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("month_"))
def handle_button_press(call :CallbackQuery):
    month=(call.data.split('_')[1])
    text="کدام نوع تراکنش؟"
    markup=InlineKeyboardMarkup(row_width=2)
    btn1=InlineKeyboardButton(text="تراکنش های تایید شده",callback_data=f"income_approved_{month}")
    btn2=InlineKeyboardButton(text="تمام تراکنش ها",callback_data=f"income_all_{month}")
    markup.add(btn1,btn2)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("income_approved_"))
def handle_button_press(call :CallbackQuery):
    if not check_admin(call.from_user.id):
            bot.send_message(chat_id=call.message.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    month=int(call.data.split('_')[2])
    print(call.data)
    income=get_month_income_approved(year="2024",month=f"{month}")
    # income=10#! remove it

    text=f"""درامد شما در ماه {months[month]},{month} 
برابر است با : <a>{income}</a>
    """
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )

@bot.callback_query_handler(func=lambda call: call.data.startswith("income_all_"))
def handle_button_press(call :CallbackQuery):
    if not check_admin(call.message.from_user.id):
            bot.send_message(chat_id=call.message.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    month=int(call.data.split('_')[2])
    print(month)
    income=get_month_income(year="2024",month=f"{month}")
    # income=10#! remove it
    text=f"""درامد شما در ماه 
    {months[month]},{month} 
برابر است با : <a>{income}</a>
    """
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )


#!#########################
# for making bot running
if __name__ == "__main__":
    start_scheduler()
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    # send_startup_message()
    bot.polling()
# bot.close()