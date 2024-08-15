import time
import schedule
import threading
import logging
from datetime import datetime
from telebot import TeleBot , custom_filters
from configs.auth import *
from database.db_creation import create_database
from database.db_functions import admin_accept_banner, admin_deny_banner, make_reserve_transaction
from database.db_timing import *
from database.db_transactions import *
from database.db_reserve import *
from database.db_users import create_user, decrease_balance, delete_user, get_all_users, get_user_id, get_user_score, increase_balance, increase_score
from message_and_text.bot_message_functions import *
from message_and_text.bot_messages import *
from message_and_text.text import *
from Markups import *
from states import *
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from functions.custom_functions import *

########################################################################
state_storage=StateMemoryStorage()
bot =TeleBot(token = TOKEN,state_storage=state_storage, parse_mode="HTML")
########################################
#* restart  msg
def restartMessageToAdmins():
    text=f'bot is started at : {get_current_datetime()}'
    for admin in ADMIN_ID_LIST:
        bot.send_message(chat_id=admin,text=text)     
########################################

#* user state in channels
def isMemberOf(user_id,channel):
    is_member=bot.get_chat_member(chat_id=channel,user_id=user_id)
    if is_member.status in ['left','kicked']:
        return False
    return True
#* user state in channels
def isMemberOfChannels(user_id,channels=CHANNELS_USERNAME):
    for channel in channels:
        is_member=bot.get_chat_member(chat_id=channel,user_id=user_id)
        if is_member.status in ['left','kicked']:
            return False
        return True
#* join and mem check handler 
def isInDB(user_id):
    # bot.send_message(user_id,text=reboot_text,reply_markup=ReplyKeyboardRemove())
    is_in_DB= get_user_id(user_id=user_id)
    if is_in_DB:
        return True
    return False


def botNeedReboot(user_id):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(restart_markup_text)
    bot.send_message(chat_id=user_id,text=bot_need_reboot_msg,reply_markup=markup)
########################################
#* user check handler
def user_check_handler(user_id,username):
    """check both user is in db and user is member of channels
    and send a custom message and markup for each 
    """
    is_member= isMemberOfChannels(user_id=user_id)
    if not is_member:
        markup=makeJoinChannelMarkup(user_id=user_id)
        bot.send_message(chat_id=user_id,text=not_member_msg,reply_markup=markup)
        return False
    is_in_db= isInDB(user_id=user_id)
    # print(is_in_db)
    if not is_in_db:
        create_user(userid=user_id,username=username)
        result= isInDB(user_id=user_id)
        if not result:
            markup=ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(restart_markup_text)
            bot.send_message(chat_id=user_id,text=not_in_db_msg,reply_markup=markup)
            return False
    return True        

########################################
#callback query for join
@bot.callback_query_handler(func=lambda call:call.data=="proceed")
def proceed (call :CallbackQuery):
    user_id=call.message.chat.id
    username=call.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if user_check:
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(chat_id=user_id,text=joined_msg,reply_markup=markup_main)


########################################################################
#* /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
        bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
        
        username=msg.from_user.username
        user_id=msg.from_user.id
        user_check= user_check_handler(user_id=user_id,username=username)
        if not user_check:
            return False
        else:
            bot.send_message(chat_id=msg.chat.id,text=new_user_text,reply_markup=markup_main)
#?#######################################################################
#* make banner
@bot.message_handler(func=lambda m:m.text == make_banner_btn)
def start(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

    user_id=msg.chat.id
    username=msg.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
        ##  botNeedReboot(user_id=user_id)
        return False
    text=f"برای ساخت بنر روی دکمه زیر کلیک کنید"
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="ساخت بنر",callback_data=f"make_banner")
    markup.add(btn)
    bot.send_message(chat_id=user_id,text=text,reply_markup=markup)
    
#?#######################################################################
#* user account btn
@bot.message_handler(func=lambda m:m.text == user_acc_btn)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
        ##  botNeedReboot(user_id=user_id)
        return False
    balance= get_user_balance(user_id)
    score=get_user_score(user_id)
    text=make_user_info(user_id=user_id,balance=balance,score=score,username=msg.from_user.username)
    markup=InlineKeyboardMarkup(row_width=1)
    btn=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
    markup.add(btn)
    bot.send_message(user_id,text=text,reply_markup=markup)
#?#######################################################################
#*balance inc btn
@bot.callback_query_handler(func=lambda call: call.data == "user_balance_inc")
def user_balance_inc(call : CallbackQuery):

    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
        ##  botNeedReboot(user_id=user_id)
        return False
    markup=InlineKeyboardMarkup()
    for index,plan in enumerate(increase_plans_btn_text,start=0):#make btn for plans
        btn=InlineKeyboardButton(text=plan,callback_data=f"plan_{index}")
        markup.add(btn)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=increase_balance_msg,reply_markup=markup)
########################################################################
#balance inc handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("plan_"))
def handle_button_press(call :CallbackQuery):
    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
       # #  botNeedReboot(user_id=user_id)
        return False
    index=int(call.data.split('_')[1])
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="ارسال رسید",callback_data=f"send_receipt_{index}")
    markup.add(btn)
    text=select_plan_msg(index=index)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)
########################################################################
#get pic_receipt
@bot.callback_query_handler(func= lambda m:m.data.startswith("send_receipt_"))
def handle_button_press(call:CallbackQuery):
    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
        return False
    index=int(call.data.split('_')[2])
    text=get_pic_receipt_msg(index)
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=user_state.pic_receipt,chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['plan'] = index


########################################################################
# # send pic for admin 
@bot.message_handler(state=user_state.pic_receipt,content_types=['photo'])
def forward(msg : Message):
    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
        return False
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
balance of user : {get_user_balance(user_id=msg.from_user.id)}
balance increase amount:‌ {plans[index]}  H T
""",reply_markup=markup,reply_to_message_id=forwarded_msg.message_id)
    # bot.send_message(chat_id=ADMIN_ID_LIST[0],text=f"------------------------------",reply_to_message_id=forwarded_msg.message_id)
    bot.send_message(msg.chat.id,text=text)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)


########################################################################

#?#######################################################################
#accept btn
@bot.callback_query_handler(func= lambda m:m.data =="pic_receipt_accept")
def admin_accept_banner_btn(call :CallbackQuery):
    user_id=(find_pattern_id(call.message.text))
    info_text=call.message.text
    amount=int(find_pattern_balance_amount(info_text))
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش تایید شد",callback_data="!?!?!?!")
    markup.add(btn)
    try:
        increase_balance(user_id=user_id,increase_amount=amount)
        add_transactions(approve=1,amount=amount,user_id=int(user_id),user_name=call.from_user.username,record_date=current_date(),record_time=get_current_time())
        for index,price in enumerate(price_plans, start=1):
            if amount == price :
                increase_score(user_id=user_id,increase_amount=index)
        new_balance=get_user_balance(user_id=user_id)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"{info_text} \n -----------\nnew amount: {new_balance} HT",reply_markup=markup)
        bot.send_message(chat_id=user_id,text=f"تراکنش شما تایید و حساب شما شارژ شد  \n برای مشاهده موجودی خود از دکمه '{user_acc_btn}' استفاده کنید") 
    except Error as e:
        logging.error(f"admin_accept_banner_btn : {e}")
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی در اپدیت موجودی کاربر پیش امده است")
#?#######################################################################
#deny btn
@bot.callback_query_handler(func= lambda m:m.data =="pic_receipt_deny")
def admin_deny(call :CallbackQuery):
    user_id=(find_pattern_id(call.message.text))
    text=call.message.text
    info_text=call.message.text
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن تراکنش را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)
    amount=int(find_pattern_balance_amount(info_text))
    add_transactions(approve=0,amount=amount,user_id=int(user_id),user_name=call.from_user.username,record_date=current_date(),record_time=get_current_time())

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
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.chat.id,text=support_msg)
     
#?#######################################################################
#free time :day of weak
@bot.message_handler(func=lambda m:m.text == free_rime_btn)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_handler(user_id=user_id,username=username)
    if not user_check:
       #  botNeedReboot(user_id=user_id)
        return False
    markup_free_time=InlineKeyboardMarkup(row_width=2) 
    current_time=get_current_time()
    # print(current_time)
    if compare_time("00:00",current_time) and compare_time(current_time,"02:00"):
        batten_test=InlineKeyboardButton(text=f"{cal_day(-1)} : {gregorian_to_jalali(cal_date(-1))}",callback_data=f"time_btn_-1")
        markup_free_time.add(batten_test)
    for i in range(7):
        batten_test=InlineKeyboardButton(text=f"{cal_day(i)} : {gregorian_to_jalali(cal_date(i))}",callback_data=f"time_btn_{i}")
        markup_free_time.add(batten_test)

    text=f"از لیست زیر می توانید روز مورد نظر را برای دریافت ساعت های خالی انتخاب کنید \n امروز {cal_day(0)} : {gregorian_to_jalali(cal_date(0))} "
    bot.send_message(chat_id=msg.chat.id,text=text,reply_markup=markup_free_time)


########################################################################
#free time handler : show times of day
@bot.callback_query_handler(func=lambda call: call.data.startswith("time_btn_"))
def handle_button_press(call :CallbackQuery):
     user_id=call.from_user.id
     result_member = isInDB(user_id=user_id)
     if result_member:
        day=int(call.data.split('_')[2])
        # print(day,cal_day(day))
        make_day=cal_date(day)
        #todo:check is update
        #todo:except and try reverse
        created = create_channel_timing(make_day)
        try:
            result =get_day_reserves(day)
            # #show result
            markup_reserve=InlineKeyboardMarkup()
            btn_reserve=InlineKeyboardButton(text=f"رزرو لینک برای تاریخ:{gregorian_to_jalali(cal_date(day))}",callback_data=f"reserve_{day}_{cal_date(day)}")
            markup_reserve.add(btn_reserve)
            from_admin=check_is_admin(user_id=user_id)
            text=make_timing_of_day_msg(result,day,from_admin=from_admin)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup_reserve,parse_mode="HTML")#todo:remove html
        except:
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی پیش امده لطفا دوباره تلاش کنید",reply_markup=ReplyKeyboardRemove())

         
    
################################################
# hour's reserve  handler : select times
@bot.callback_query_handler(func=lambda call: call.data.startswith("reserve_"))
def handle_button_press(call :CallbackQuery):
     user_id=call.from_user.id
     result_member = isInDB(user_id=user_id)
     if result_member:
        day=int(call.data.split('_')[1])
        date=(call.data.split('_')[2])
        result =get_day_reserves(day)
        result=list(result)
        markup=InlineKeyboardMarkup(row_width=4)
        buttons=[]
        current_time=get_current_time();
        current_time=add_time(current_time,interval_reservation_time)
        if day == 0:
            for i in range (len(time_of_day)):
                if not compare_time(time1=current_time,time2=time_of_day[i]): # if time is past
                    if compare_time(time1=current_time,time2="23:59") and compare_time (time1=time_of_day[i],time2="02:01"):
                        continue
                    result[(i+1)]=1
        if day==-1:
            for i in range (len(time_of_day)):
                if i< 18:
                    result[(i+1)]=1
                    continue
                # print(current_time,time_of_day[i])
                if not compare_time(time1= current_time,time2= time_of_day[i]): # if time is past
                    result[(i+1)]=1
        for i in range (len(time_of_day)):
            if result[(i+1)] == 0:# if time is full dont show it
                btn_day_reserve=InlineKeyboardButton(text=time_of_day[i],callback_data=f"day_{day}_{i}")
                buttons.append(btn_day_reserve)
        for i in range(0, len(buttons), 3):
            markup.row(*buttons[i:i+3])
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                            text=f" ساعت های خالی برای \n  {cal_day(day)} , معادل : {gregorian_to_jalali(date)}",reply_markup=markup)
################################################
# reserve handler : reserve info 
@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def handle_button_press(call:CallbackQuery):
     user_id=call.from_user.id
     result_member = isInDB(user_id=user_id)
     if result_member:
     #todo: make sure time is available
     #todo: get link from user, and scheduling it
        day=int(call.data.split('_')[1]) # it is a number in range(0 to 6)
        time=int(call.data.split('_')[2]) # its number , use 'time_of_day[time]'
        user_balance=int(get_user_balance(user_id=user_id))
        price= price_1 if time <5 else price_2 if 5<=time< 21 else price_3
        text=f"{make_reserve_info_text(day=cal_day(day),date=gregorian_to_jalali(cal_date(day)),time=time_of_day[time],price=price)}  \n{make_line} \n موجودی حساب شما : {user_balance} هزار تومان"
        markup_balance_low=InlineKeyboardMarkup()
        btn=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
        btn1=InlineKeyboardButton(text="موجودی حساب شما کافی نیست",callback_data=f"send_link_{day}_{time}")
        markup_balance_low.add(btn1)
        markup_balance_low.add(btn)
        markup_ok=InlineKeyboardMarkup()
        btn2=InlineKeyboardButton(text="تایید و ارسال بنر",callback_data=f"get_banner_{day}_{time}")
        btn3=InlineKeyboardButton(text="  ساخت بنر",callback_data=f"make_banner")
        markup_ok.add(btn3,btn2)
        if user_balance >= price:
            markup=markup_ok
        else:
            markup=markup_balance_low
            # bot.send_message(chat_id=user_id,text=f"برای شارژ حساب خود از دکمه '{user_acc_btn}' استفاده کنید")
        bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)
#?##############################################
# ساخت بنر
@bot.callback_query_handler(func=lambda call: call.data== "make_banner")
def handle_button_press(call:CallbackQuery):
     user_id=call.from_user.id
     result_member = isInDB(user_id=user_id)
     if result_member:
      bot.send_message(chat_id=call.message.chat.id,text=f"اسم گروه شما چیست؟ \n حداکثر {max_len_name} کاراکتر")
      bot.set_state(user_id=call.message.chat.id,state=banner_state.name,chat_id=call.message.chat.id)
     
#?##############################################
# تایید و ارسال بنر
@bot.callback_query_handler(func=lambda call: call.data.startswith("get_banner_"))
def get_banner_from_user(call:CallbackQuery):
    user_id=call.from_user.id
    day=int(call.data.split('_')[2]) # it is a number in range(0 to 6)
    time=int(call.data.split('_')[3]) # its number , use 'time_of_day[time]'
    price= price_1 if time <5 else price_2 if 5<=time< 21 else price_3
    call_text=call.message.text
    # info_text=f"info: {time}_{day}_{price}"
    result_member = isInDB(user_id=user_id)
    if result_member:
        text=f"""{call_text}
لطفا بنر خود را برای ما ارسال کنید
در صورتی که بنر چنل ما را ندارید لطفا از دکمه '{make_banner_btn}' استفاده کنید"""
        bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.set_state(user_id=call.message.chat.id,state=banner_state.banner,chat_id=call.message.chat.id)
        with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
          data['day'] = day
          data['date'] = cal_date(day)
          data['time'] = time
          data['price'] = price
#################
#دریافت بنر و ایجاد رزرو
@bot.message_handler(state =banner_state.banner)
def get_banner(msg : Message):    # Split the text into lines
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
          day=data['day'] 
          date=data['date'] 
          time_index=data['time'] 
          price=data['price'] 
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    banner=msg.text
    user_id=msg.from_user.id
    username=msg.from_user.username
    if is_banner_ok(banner=banner):
        link=extract_link(banner)
        try:#* decrease balance , make time full , make reserve
            make_reserve_transaction(user_id=user_id,price=price,time_index=time_index,date=date,banner=banner,link=link)
        except Error as e:
            bot.send_message(chat_id=msg.from_user.id,text="مشکلی پیش امده است لطفا مجدد تلاش کنید")
            logging.error(f"\033[91m error 'get_banner' from user: \n {e} \n \033[0m")

        markup=InlineKeyboardMarkup()
        btn1=InlineKeyboardButton(text="تایید",callback_data="banner_accept")
        btn2=InlineKeyboardButton(text="رد کردن",callback_data="banner_deny")
        btn3=InlineKeyboardButton(text="تغییر بنر",callback_data="banner_custom")
        markup.add(btn1,btn2)
        markup.add(btn3)
        forwarded_msg=bot.forward_message(chat_id=ADMIN_ID_LIST[0],from_chat_id=msg.chat.id,message_id=msg.message_id)
        reserve_id=get_id_with_time_date_reserve(time=time_of_day[time_index],date=date)
        text=make_banner_acc_msg_to_admin(username=username,user_id=user_id,time=time_index,day=day,price=price,reserve_id=reserve_id[0])
        bot.send_message(chat_id=ADMIN_ID_LIST[0],text=text,reply_markup=markup,reply_to_message_id=forwarded_msg.message_id)
        bot.send_message(chat_id=msg.from_user.id,text=forward_banner_text)

    else:
        bot.send_message(msg.from_user.id,text=banner_not_mach)
###
#deny btn  #todo:return balance to user
@bot.callback_query_handler(func= lambda m:m.data =="banner_deny")
def admin_deny(call :CallbackQuery):
    info=call.message.text
    user_id=(find_pattern_id(info))
    reserve_id=get_reserve_id(info)
    DATA=parse_text_for_acc_admin_banner(info)
    # print(reserve_id)
    time_index=int(DATA['time'])
    date=DATA['date']
    price=int(DATA['price'])
    try:
        admin_deny_banner(user_id=user_id,price=price,time_index=time_index,date=date,reserve_id=reserve_id)
    except Error as e:
        logging.error(f"\033[91m error 'admin_deny' banner: \n {e} \n \033[0m")
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"مشکلی پیش امد دوباره تلاش کنید \n {make_line} \n{text}")



    text=call.message.text
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این رزرو رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن رزرو را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)
    bot.send_message(chat_id=user_id,text=f"رزرو شما از سمت ادمین رد شد \n درصورت نیاز میتوانید با استفاده از دکمه '{support_btn}' با ادمین ارتباط برقرار کنید")
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)
#######
#accept btn
@bot.callback_query_handler(func= lambda m:m.data =="banner_accept")
def admin_accept_banner_btn(call :CallbackQuery):
    info_text=call.message.text
    data=parse_text_for_acc_admin_banner(info_text)
    date=data['date']
    time_index=int(data['time'])
    user_id=data['user_id']
    reserve_id=int(data['reserve_id'])
    data['banner']=call.message.reply_to_message.message_id
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این رزرو تایید شد",callback_data="!?!?!?!")
    markup.add(btn)
    try:
        admin_accept_banner(user_id=user_id,time_index=time_index,reserve_id=reserve_id,date=date)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"{info_text} \n {make_line} \n بنر تایید شد",reply_markup=markup)
        bot.send_message(chat_id=user_id,text="بنر شما تایید و در ساعت انتخاب شده گذاشته میشود") 
    except Error as e:
        logging.error(f"\033[91m Error admin_accept_banner_btn: \n {e} \n \033[0m")
        btn=InlineKeyboardButton(text="تایید مجدد",callback_data="banner_accept")
        markup.add(btn)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی در اپدیت موجودی کاربر پیش امده است",reply_markup=markup)
#?###############################################################################
#* make banner  section
@bot.message_handler(state =banner_state.name)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        name=data['name']=msg.text
     if len(name) > max_len_name:
        bot.send_message(text=f"تعداد کارکتر وارد شده برای نام : {len(name)} \n حداکثر مجاز :{max_len_name} \n لطفا دوباره تلاش کنید",chat_id=msg.chat.id)
        return
     bot.send_message(text=f"تعداد اعضای گروه شما چند نفر است \n حداکثر {max_len_member} کاراکتر",chat_id=msg.chat.id)
     bot.set_state(state=banner_state.member,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.member)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
       member= data['member']=msg.text
       if len(member) > max_len_member:
            bot.send_message(text=f"تعداد کارکتر وارد شده برای نام : {len(member)} \n حداکثر مجاز :{max_len_member} \n لطفا دوباره تلاش کنید",chat_id=msg.chat.id)
            return
     bot.send_message(text=f"در یک خط اگر توضیحاتی لازم است برای گروه خود بنویسید \n حداکثر {max_len_des} کاراکتر",chat_id=msg.chat.id)
     bot.set_state(state=banner_state.description,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.description)
def make_banner(msg : Message):
     with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        des=data['description']=msg.text
     if len(des) > max_len_des:
        bot.send_message(text=f"تعداد کارکتر وارد شده برای نام : {len(des)} \n حداکثر مجاز :{max_len_des} \n لطفا دوباره تلاش کنید",chat_id=msg.chat.id)
        return
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
     banner= make_channel_banner(name=name,members=member,description=description,link=link)
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
        if check_is_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text="خوش امدی ادمین",reply_markup=markup_main_admin)
        else:
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
##########################
#* user list
#todo : paging
@bot.message_handler(func=lambda m:m.text == admin_btn_user_list)
def user_list(msg : Message):
     if not check_is_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
     users=get_all_users()
     markup = InlineKeyboardMarkup()
     for user in users:
         btn= InlineKeyboardButton(text=f"{user[3]}:{user[0]}",callback_data=f"users_{user[0]}")
         markup.add(btn)
     bot.send_message(chat_id=msg.chat.id,text="لیست کاربر ها",reply_markup=markup)
##########################
#* find user
@bot.message_handler(func=lambda m:m.text == admin_btn_find_user_info)
def find_user(msg : Message):
    admin_id=msg.from_user.id
    bot.set_state(user_id=msg.from_user.id,state=admin_state.find_user,chat_id=msg.chat.id)
    bot.send_message(admin_id,"user_id کاربر مد نظر را ارسال کنید")
#############33
@bot.message_handler(state=admin_state.find_user)
def get_user_info_admin(msg:Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    user_id=msg.text
    balance=get_user_balance(user_id)
    score=get_user_score(user_id)
    text=f"id: {user_id}\n{make_user_info(user_id=user_id,balance=balance,score=score)}"
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=admin_btn_increase_balance,callback_data=admin_btn_increase_balance)
    btn2=InlineKeyboardButton(text=admin_btn_decrease_balance,callback_data=admin_btn_decrease_balance)
    btn3=InlineKeyboardButton(text=admin_btn_increase_score,callback_data=admin_btn_increase_score)
    btn4=InlineKeyboardButton(text=admin_btn_decrease_score,callback_data=admin_btn_decrease_score)
    btn5=InlineKeyboardButton(text=admin_btn_msg_user,callback_data=admin_btn_msg_user)
    btn6=InlineKeyboardButton(text=admin_btn_delete_user,callback_data=admin_btn_delete_user)
    markup.add(btn1,btn2)
    markup.add(btn3,btn4)
    markup.add(btn5,btn6)
    bot.edit_message_text(chat_id=msg.chat.id,message_id=msg.message_id,text=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data== admin_btn_delete_user)
def handle_button_press(call :CallbackQuery):
    text=call.message.text
    try:
        user_id=find_pattern_id(text)
        delete_user(user_id)
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="کاربر پاک شد",callback_data="2134"))
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)
    except Error as e:
        logging.error(f"\033[91merror delete a user: \n {e} \n \033[0m")
        bot.send_message(call.message.from_user.id,text="مجدد تلاش کنید کاربر پاک نشد")
        


##########################
#* bot info
@bot.message_handler(func=lambda m:m.text == admin_btn_bot_info)
def user_list(msg : Message):
     if not check_is_admin(msg.from_user.id):
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
    if not check_is_admin(call.message.from_user.id):
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
    if not check_is_admin(msg.from_user.id):
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
     if not check_is_admin(msg.from_user.id):
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
    if not check_is_admin(call.from_user.id):
            bot.send_message(chat_id=call.message.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    month=int(call.data.split('_')[2])
    # print(call.data)
    income=get_month_income_approved(year="2024",month=f"{month}")
    # income=10#! remove it

    text=f"""درامد شما در ماه {months[month]},{month} 
برابر است با : <a>{income}</a>
    """
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )

@bot.callback_query_handler(func=lambda call: call.data.startswith("income_all_"))
def handle_button_press(call :CallbackQuery):
    if not check_is_admin(call.message.from_user.id):
            bot.send_message(chat_id=call.message.chat.id,text=not_admin_text,reply_markup=markup_main)
            return False
    month=int(call.data.split('_')[2])
    # print(month)
    income=get_month_income(year="2024",month=f"{month}")
    # income=10#! remove it
    text=f"""درامد شما در ماه 
    {months[month]},{month} 
برابر است با : <a>{income}</a>
    """
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )
##########################
#! error handler
# بخش دریافت رسید از کاربر
@bot.message_handler(state=user_state.pic_receipt, content_types=['text', 'video', 'document', 'audio', 'sticker', 'voice', 'location', 'contact'])
def handle_non_photo(msg: Message):
    # پیام خطا برای ارسال محتوای غیر از عکس
    bot.send_message(msg.chat.id, "لطفاً فقط یک عکس از رسید خود ارسال کنید.")


#!#########################
#todo: test section #######################################################################

# # /test
@bot.message_handler(commands=['test'])
def test(msg : Message):
    link='+HJAazmF_lDtlODI0'
    # if link.startswith('https://t.me/'):
        # link = link[len('https://t.me/'):]
    try:
        chat_id_or_username = link
        chat_info = bot.get_chat(chat_id_or_username)
        print(chat_info)
    except:
        print()
    # bot.send_message(msg.from_user.id,text=chat_info)


################################################
def send_scheduled_message():
    bot.send_message(chat_id=ADMIN_ID_LIST[0],text=f"schedule_jobs : {get_current_time()}")

    # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # text = f"این یک پیام زمان‌بندی‌شده است که در {current_time} ارسال شده است."
    # bot.send_message(ADMIN_ID_LIST[1], text)
    time=datetime.now().strftime('%H:%M')
    # print(time)
    time_index=find_index(time,time_of_day)
    date=get_current_date()
    user_id=get_id_reserver(time=time,date=date)
    if user_id is not None :
        user_id=int(user_id[0])
        bot.send_message(ADMIN_ID_LIST[0],text=f"time:{time} : date:{date}\n user_id:{user_id}")
        if user_id != 1 :
            reserve_id=get_id_with_time_date_reserve(time=time,date=date)[0]
            banner=get_banner_with_id_reserve(reserve_id)[0]
            for channel in CHANNELS_USERNAME:
                bot.send_message(chat_id=channel,text=banner,disable_web_page_preview=True,link_preview_options=False)
                bot.send_message(ADMIN_ID_LIST[0],text="یک بنر ارسال شد")
            
            

    # bot.send_message(CHANNELS_USERNAME[1],text)
    # print(f"پیام در {current_time} ارسال شد.")

##############################################
def schedule_jobs():
    schedule.clear()
    for i in range(len(time_of_day)):
        schedule.every().day.at(time_of_day[i]).do(send_scheduled_message)
#################################################
def schedule_jobs_test():
    schedule.clear()
    for i in range(10):
        schedule.every().day.at(f"23:1{i}").do(send_scheduled_message)

#################################################
# تابع برای اجرای زمان‌بندی
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    schedule_jobs()
    # schedule_jobs_test()  # ثبت وظایف زمان‌بندی‌شده
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True  # این کار باعث می‌شود Thread با بستن برنامه اصلی بسته شود
    scheduler_thread.start()

#!#########################
#هر پیامی از کاربر
@bot.message_handler(func=lambda message: True)
def handle_non_photo(msg: Message):
    markup=ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(restart_markup_text)
    bot.send_message(msg.chat.id, "لطفا برای استفاده از ربات یا از دکمه های ربات استفاده کنید یا مجدد ربات را راه اندازی کنید",reply_markup=markup)


# for making bot running
if __name__ == "__main__":
    try:
        # تنظیمات اولیه لاگ‌گیری
        log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logging.info("ربات در حال اجراست...")
        create_database() # DATA BASE
        restartMessageToAdmins() # hello message
        start_scheduler() # auto send post 
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.polling() # keep bot running
    except Exception as e:
        logging.error(f"خطا در اجرای ربات: {e}")
# bot.close()



