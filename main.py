import logging
from datetime import datetime
from telebot import TeleBot , custom_filters,apihelper
from configs.auth import *
from database.db_creation import dbCreateDatabases
from database.db_functions import db_set_new_cart, make_reserve_transaction_weak_reserve, transactions_admin_accept_banner, admin_deny_banner, db_convert_score, make_reserve_transaction, transactions_admin_accept_banner_weak_reserve
from database.db_timing import *
from database.db_transactions import *
from database.db_setting import *
from database.db_reserve import *
from database.db_users import db_user_insert, db_user_is_exist, decrease_balance, decrease_score, delete_user, get_all_users, get_users_count, user_exist, get_user_score, increase_balance, increase_score
from functions.calender_functions import add_date, add_time, compare_date, compare_dates, compare_time, date_is_past, compare_date_is_eq, get_current_date, get_current_datetime, get_current_time, is_difference_less_than_15_minutes
from functions.format_patern import text_is_cart_number
from functions.log_functions import get_last_errors, get_latest_log_file, remove_old_logs, test_logError
from functions.sched_functions import start_scheduler
from message_and_text.bot_message_functions import *
from message_and_text.bot_messages import *
from message_and_text.text import *
from Markups import *
from states import *
from telebot.storage import StateMemoryStorage
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove
from functions.custom_functions import *
#######################################
state_storage=StateMemoryStorage()
bot =TeleBot(token = BOT_TOKEN,state_storage=state_storage, parse_mode="HTML")
bot_is_enable=True 
#######################################
banner_need_approve=True
disable_notification=True
#######################################* function for Management
def user_check_DB_and_membership(user_id, username, channels=CHANNELS_USERNAME, admin_id=SUPPORT_ID):
    """
    Checks if the user is a member of required channels and if the user exists in the database.
    Sends appropriate messages and markup in case of issues.
    """
    try:
        # Step 1: Check if the user is a member of the specified channels
        for channel in channels:
            try:
                # Check if the user is a member of the current channel
                is_member = bot.get_chat_member(chat_id=channel, user_id=user_id)
                if is_member.status in ['left', 'kicked']:
                    # User is not a member of the channel
                    markup = makeJoinChannelMarkup(user_id=user_id)
                    bot.send_message(chat_id=user_id, text=msg_not_member, reply_markup=markup)
                    return False

            except apihelper.ApiTelegramException as e:
                # Handle all Telegram API exceptions
                if e.result.status_code == 403:  # Forbidden: Bot has no access to the channel
                    bot.send_message(chat_id=admin_id, 
                                     text=f"❗️ The bot has no access to channel {channel}. Please check the access.")
                elif e.result.status_code == 400:  # Bad Request (e.g., invalid chat_id)
                    bot.send_message(chat_id=admin_id, 
                                     text=f"⚠️ Error: Channel {channel} is invalid or user ID {user_id} is incorrect.")
                else:
                    # Handle other API-related errors
                    bot.send_message(chat_id=admin_id, 
                                     text=f"⚠️ Error checking channel {channel} for user {user_id}: {e.description}")
                    logging.error(f"Error checking channel {channel} for user {user_id}: {e}")

                return False

            except Exception as e:
                # Handle general exceptions (e.g., network errors, system resource access issues)
                bot.send_message(chat_id=admin_id, 
                                 text=f"⚠️ A system error occurred while checking channel {channel}: {str(e)}")
                logging.error(f"Unexpected error checking channel {channel} for user {user_id}: {e}")
                return False

        # Step 2: Check if the user is already in the database
        if not db_user_is_exist(user_id=user_id):
            # If not in the database, attempt to create a new user entry
            db_user_insert(userid=user_id, username=username)
            result = db_user_is_exist(user_id=user_id)
            if not result:
                # User creation failed; send appropriate message with restart option
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(restart_markup_text)
                bot.send_message(chat_id=user_id, text=msg_not_in_db, reply_markup=markup)
                return False

        return True

    except Exception as e:
        # Catch any unexpected errors and log them
        logging.error(f"Unexpected error in user check and membership function for user {user_id}: {e}")
        bot.send_message(chat_id=admin_id, 
                         text=f"⚠️ An unexpected error occurred for user {user_id}: {str(e)}")
        return False
#######################################























































########################################* USER Section ( markup and call back data and .. )
# /start
@bot.message_handler(commands=['start'])
def start(msg : Message):
        bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
        
        username=msg.from_user.username
        user_id=msg.from_user.id
        user_check= user_check_DB_and_membership(user_id=user_id,username=username)
        if not user_check:
            return False
        else:
            bot.send_message(chat_id=msg.chat.id,text=msg_start_command,reply_markup=markup_user_main)
###############
#callback query for join
@bot.callback_query_handler(func=lambda call:call.data=="proceed")
def proceed (call :CallbackQuery):
    user_id=call.message.chat.id
    username=call.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if user_check:
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(chat_id=user_id,text=msg_joined,reply_markup=markup_user_main)
#############################################
#make banner
@bot.message_handler(func=lambda m:m.text == markup_user_make_banner)
def start(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    if  not bot_is_enable:
         send_bot_is_disable_text_to_user(user_id=msg.from_user.id) 
         return

    user_id=msg.chat.id
    username=msg.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)

    if not user_check:
        return False
    
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="ساخت بنر",callback_data=f"make_banner")
    markup.add(btn)
    bot.send_message(chat_id=user_id,text=msg_make_banner,reply_markup=markup)
############################################# 
# user account btn
@bot.message_handler(func=lambda m:m.text == markup_user_account_btn)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    if  not bot_is_enable:
         send_bot_is_disable_text_to_user(user_id=msg.from_user.id) 
         return


    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    balance= get_user_balance(user_id)
    score=get_user_score(user_id)
    text=make_user_info(user_id=user_id,balance=balance,score=score,username=msg.from_user.username)
    markup=InlineKeyboardMarkup(row_width=1)
    btn=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
    markup.add(btn)
    bot.send_message(user_id,text=text,reply_markup=markup)
###############
#markup balance increase btn
@bot.callback_query_handler(func=lambda call: call.data == "user_balance_inc")
def user_balance_inc(call : CallbackQuery):

    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    markup=InlineKeyboardMarkup()
    for index,plan in enumerate(increase_plans_btn_text,start=0):
        btn=InlineKeyboardButton(text=plan,callback_data=f"plan_{index}")
        markup.add(btn)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=increase_balance_msg,reply_markup=markup)
###############
#balance increase  : selected a plan 
@bot.callback_query_handler(func=lambda call: call.data.startswith("plan_"))
def handle_button_press(call :CallbackQuery):
    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    index=int(call.data.split('_')[1])
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="ارسال رسید",callback_data=f"send_receipt_{index}")
    markup.add(btn)
    text=select_plan_msg(index=index)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)
##############################
#balance increase:get pic_receipt
@bot.callback_query_handler(func= lambda m:m.data.startswith("send_receipt_"))
def handle_button_press(call:CallbackQuery):
    user_id=call.from_user.id
    username=call.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    index=int(call.data.split('_')[2])
    text=get_pic_receipt_msg(index)
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    bot.send_message(chat_id=call.message.chat.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=user_state.pic_receipt,chat_id=call.message.chat.id)

    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['plan'] = index
###############
#balance increase: send pic for admin 
@bot.message_handler(state=user_state.pic_receipt,content_types=['photo'])
def forward(msg : Message):
    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    text=f"رسید شما برای ادمین ارسال شد و تا ساعاتی دیگر مورد تایید قرار میگرد \n و پس از ان حساب شما شارژ میشود"
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text="تایید",callback_data="pic_receipt_accept")
    btn2=InlineKeyboardButton(text="رد کردن",callback_data="pic_receipt_deny")
    markup.add(btn1,btn2)
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        index = int(data.get('plan'))
    forwarded_msg=bot.forward_message(chat_id=ADMIN_ID_LIST[0],from_chat_id=msg.chat.id,message_id=msg.message_id)

    bot.send_message(chat_id=ADMIN_ID_LIST[0],text=f"""id: {msg.from_user.id} ,
username: @{msg.from_user.username} 
balance of user : {get_user_balance(user_id=msg.from_user.id)}
balance increase amount:‌ {plans[index]}  H T 💵
""",reply_markup=markup,reply_to_message_id=forwarded_msg.message_id,disable_notification=disable_notification)
    bot.send_message(msg.chat.id,text=text)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

###############
#balance increase accept pic btn 
@bot.callback_query_handler(func= lambda m:m.data =="pic_receipt_accept")
def admin_accept_banner_btn(call :CallbackQuery):
    user_id=(find_pattern_id(call.message.text))
    info_text=call.message.text
    amount=int(find_pattern_balance_amount(info_text))
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این تراکنش تایید شد",callback_data="!?!?!?!")
    markup.add(btn)
    try:
        for index ,price in enumerate(plans_off,start=0):
            if int(price) == int(amount):
                amount=int(plans_off_real[index])

        increase_balance(user_id=user_id,increase_amount=amount)
        add_transactions(approve=1,amount=amount,user_id=int(user_id),user_name=call.from_user.username,record_date=get_current_date(),record_time=get_current_time())
        for index,price in enumerate(price_plans, start=1):
            if amount == price :
                increase_score(user_id=user_id,increase_amount=index)
        new_balance=get_user_balance(user_id=user_id)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"{info_text} \n -----------\nnew amount: {new_balance} HT",reply_markup=markup)
        bot.send_message(chat_id=user_id,text=f"تراکنش شما تایید و حساب شما شارژ شد  \n برای مشاهده موجودی خود از دکمه '{markup_user_account_btn}' استفاده کنید") 
    except Error as e:
        logging.error(f"admin_accept_banner_btn : {e}")
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی در اپدیت موجودی کاربر پیش امده است")

###############
#balance increase : deny btn
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
    add_transactions(approve=0,amount=amount,user_id=int(user_id),user_name=call.from_user.username,record_date=get_current_date(),record_time=get_current_time())

    bot.send_message(chat_id=user_id,text=f"تراکنش شما از سمت ادمین رد شد \n درصورت نیاز میتوانید با استفاده از دکمه پشتیبانی با ادمین ارتباط برقرار کنید")
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)

###############
#balance increase : deny msg reason
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
###############
#balance increase : send deny reason
@bot.message_handler(state=admin_state.deny_reason)
def deny_reason(msg : Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = int(data.get('user_id'))
    deny_reason_msg=msg.text
    bot.send_message(chat_id=user_id,text=f"علت رد شدن تراکنش شما : \n {deny_reason_msg}")
    bot.send_message(chat_id=msg.from_user.id,text="پیام شما برای کاربر ارسال شد")
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

#############################################
#markup support btn
@bot.message_handler(func=lambda m:m.text == btn_support)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.chat.id,text=support_msg)
#############################################
#markup free time :day of weak
@bot.message_handler(func=lambda m:m.text == markup_user_free_rime)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    if  not bot_is_enable:
         send_bot_is_disable_text_to_user(user_id=msg.from_user.id) 
         return

    user_id=msg.from_user.id
    username=msg.from_user.username
    user_check= user_check_DB_and_membership(user_id=user_id,username=username)
    if not user_check:
        return False
    markup_free_time=InlineKeyboardMarkup(row_width=2) 
    current_time=get_current_time()
    # if time is between 00  and 02 day is -1 else is day 0 
    if compare_time("00:00",current_time) and compare_time(current_time,"02:00"):
        batten_test=InlineKeyboardButton(text=f"{cal_day(-1)} : {gregorian_to_jalali(cal_date(-1))}",callback_data=f"time_btn_-1")
        markup_free_time.add(batten_test)
    for i in range(7):
        batten_test=InlineKeyboardButton(text=f"{cal_day(i)} : {gregorian_to_jalali(cal_date(i))}",callback_data=f"time_btn_{i}")
        markup_free_time.add(batten_test)
    batten_test=InlineKeyboardButton(text=f"رزرو یک هفته",callback_data=f"hi_week_reserve")

    markup_free_time.add(batten_test)

    text=f" امروز : <u>{cal_day(0)}</u> معادل : 📆<u>{gregorian_to_jalali(cal_date(0))}</u>📆\n {msg_select_day} "
    bot.send_message(chat_id=msg.chat.id,text=text,reply_markup=markup_free_time)

###############
#free time handler : show times of day
@bot.callback_query_handler(func=lambda call: call.data.startswith("time_btn_"))
def handle_button_press(call :CallbackQuery):
    user_id=int(call.from_user.id)
    day=int(call.data.split('_')[2])
    make_day=cal_date(day)
    create_channel_timing(make_day)
    try:
        result =get_day_reserves(day)
        markup_reserve=InlineKeyboardMarkup()
        btn_reserve=InlineKeyboardButton(text=f"رزرو لینک برای تاریخ:{gregorian_to_jalali(cal_date(day))}",callback_data=f"reserve_{day}_{cal_date(day)}")
        markup_reserve.add(btn_reserve)
        from_admin=check_is_admin(user_id=user_id)
        text=make_timing_of_day_msg(result,day,from_admin=from_admin)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup_reserve,parse_mode="HTML")#todo:remove html
    except:
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="مشکلی پیش امده لطفا دوباره تلاش کنید",reply_markup=ReplyKeyboardRemove())

###############
# hour's reserve  handler : select times
@bot.callback_query_handler(func=lambda call: call.data.startswith("reserve_"))
def handle_button_press(call :CallbackQuery):
    user_id=call.from_user.id
    day=int(call.data.split('_')[1])
    date=(call.data.split('_')[2])
    result =get_day_reserves(day)
    result=list(result)
    markup=InlineKeyboardMarkup(row_width=4)
    buttons=[]
    current_time=get_current_time();
    current_time=add_time(current_time,time_duration_def)
    if day == 0:
        for i in range (len(dayClockArray)):
            if compare_time(lower=current_time,than="00:29"):
                if i<18:
                    result[(i+1)]=1
                    continue
            if compare_time(lower=dayClockArray[i],than=current_time): # if time is past
                if compare_time(lower=current_time,than="23:59") and compare_time (lower=dayClockArray[i],than="02:01"):
                    continue
                result[(i+1)]=1
    if day==-1:
        for i in range (len(dayClockArray)):
            if i< 18:
                result[(i+1)]=1
                continue
            if compare_time(lower=dayClockArray[i],than=current_time): # if time is past
                result[(i+1)]=1
    for i in range (len(dayClockArray)):
        if result[(i+1)] == 0:# if time is full dont show it
            btn_day_reserve=InlineKeyboardButton(text=dayClockArray[i],callback_data=f"day_{day}_{i}")
            buttons.append(btn_day_reserve)
    for i in range(0, len(buttons), 3):
        markup.row(*buttons[i:i+3])
    text=f"⏰ ساعت های خالی برای {cal_day(day)} \n📆 معادل : {gregorian_to_jalali(date)}"
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
                        text=text,reply_markup=markup)
###############
# reserve handler : reserve info 
@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def handle_button_press(call:CallbackQuery):
    user_id=call.from_user.id
    
    day=int(call.data.split('_')[1]) # it is a number in range(0 to 6)
    time=int(call.data.split('_')[2]) # its number , use 'time_of_day[time]'
    user_balance=int(get_user_balance(user_id=user_id))
    price= price_1 if time <5 else price_2 if 5<=time< 21 else price_3
    text=make_reserve_info_text(day=cal_day(day),date=gregorian_to_jalali(cal_date(day)),time=dayClockArray[time],price=price,user_balance=user_balance)
    markup_balance_low=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
    btn1=InlineKeyboardButton(text="موجودی حساب شما کافی نیست",callback_data=f"???????")
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
#*###########
# reserve for a week start from tomorrow
@bot.callback_query_handler(func=lambda call: call.data =="hi_week_reserve")
def handle_button_press(call :CallbackQuery):
    date=cal_date(1)
    insert_channel_timing_for_custom_period(start_date=date)
    free_times=db_timing_get_free_time_for_period(interval=1)#start from tomorrow
    buttons=[]
    markup=InlineKeyboardMarkup()
    
    #if time is available
    for i in range (len(dayClockArray)):
        if free_times[(i+1)] !=1:# time is full
            continue
        btn_day_reserve=InlineKeyboardButton(text=dayClockArray[i],callback_data=f"WeakReservations_{i}")
        buttons.append(btn_day_reserve)

    #reservable reply button 
    for i in range(0, len(buttons), 3):
        markup.row(*buttons[i:i+3])

    bot.edit_message_text(text=msg_available_time_for_week,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup)
###############   
#set a temp reservation for weak
@bot.callback_query_handler(func=lambda call: call.data.startswith("WeakReservations_"))
def handle_button_press(call :CallbackQuery):
    bot.set_state(user_id=call.message.chat.id,state=banner_state.week_reserve_get_banner,chat_id=call.message.chat.id)
    user_id=call.from_user.id
    time_index=int(call.data.split('_')[1]) 
    banner_time=dayClockArray[time_index]
    
    #cal start and end time for reservation of a week start from tomorrow
    date=cal_date(1)
    end_date=add_date(date,7)
    user_balance=int(get_user_balance(user_id=user_id))
    price= price_1 if time_index <5 else price_2 if 5<=time_index< 21 else price_3

    text=msg_week_msg_reservation_info(time=banner_time,start_date=gregorian_to_jalali(date),end_date=gregorian_to_jalali(end_date),user_balance=user_balance,price=(price*7))

    #check balance of user
    if   user_balance<price*7:
        markup_balance_low=InlineKeyboardMarkup()
        btn=InlineKeyboardButton(text=balance_inc_btn,callback_data="user_balance_inc")
        btn1=InlineKeyboardButton(tCext="موجودی حساب شما کافی نیست",callback_data=f"??????")
        markup_balance_low.add(btn1)
        markup_balance_low.add(btn)
        bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=markup_balance_low)
        return False

    bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id)
    bot.send_message(text=msg_pls_send_banner,chat_id=call.message.chat.id,)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['time_index']=time_index
        data['action_dateTime']=get_current_datetime()
###############
#get banner from user : weak reserve
@bot.message_handler(state =banner_state.week_reserve_get_banner)
def get_banner(msg : Message):    # Split the text into lines
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        time_index=data['time_index']
        action_dateTime=data['action_dateTime']
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

    banner=msg.text
    user_id=msg.from_user.id
    username=msg.from_user.username
    
    date=cal_date(1)
    current_time=get_current_time()

    # check for 15 min limit for reserve
    current_action=get_current_datetime()
    if not is_difference_less_than_15_minutes(action_dateTime,current_action):
        bot.send_message(user_id,text=msg_to_late_to_reserve)
        return False
    
    if not is_banner_ok(banner=banner):
        bot.send_message(user_id,text=msg_banner_not_mach)
        return False
    links=db_reserve_get_links_within_week_reserve(interval=1)
    banner_link=extract_link(banner)
    for link in links:
        if banner_link==link:
            bot.send_message(chat_id=msg.from_user.id,text=msg_link_isDuplicated_weak)
            return False
        
    current_time=add_time(initial_time=current_time,duration=time_duration_def)

    price= price_1 if time_index <5 else price_2 if 5<=time_index< 21 else price_3

    make_reserve_transaction_weak_reserve(user_id=user_id,price=price,time_index=time_index,start_date=date,banner=banner,link=banner_link)

    if banner_need_approve:
        markup=InlineKeyboardMarkup()
        btn1=InlineKeyboardButton(text="تایید",callback_data="banner_accept")
        btn2=InlineKeyboardButton(text="رد کردن",callback_data="banner_deny")
        btn3=InlineKeyboardButton(text="تغییر بنر",callback_data="banner_custom")
        markup.add(btn1,btn2)
        markup.add(btn3)
        forwarded_msg=bot.forward_message(chat_id=ADMIN_ID_LIST[0],from_chat_id=msg.chat.id,message_id=msg.message_id)
        reserve_id=int(get_id_with_time_date_reserve(time=dayClockArray[time_index],date=date))
        day=cal_day()#todo : what to do
        text=make_banner_acc_msg_to_admin(username=username,user_id=user_id,time=time_index,day=day,price=price,reserve_id=reserve_id[0])
        bot.send_message(chat_id=ADMIN_ID_LIST[0],text=text,reply_markup=markup,reply_to_message_id=forwarded_msg.message_id)
        bot.send_message(chat_id=msg.from_user.id,text=forward_banner_text,disable_notification=disable_notification)
    else:
        reserve_id=int(get_id_with_time_date_reserve(time=dayClockArray[time_index],date=date)[0])
        transactions_admin_accept_banner_weak_reserve(user_id=user_id,time_index=time_index,reserve_id=reserve_id,start_date=date)
        bot.send_message(chat_id=user_id,text=msg_banner_is_accepted) 
        
###############
#markup make banner 
@bot.callback_query_handler(func=lambda call: call.data== "make_banner")
def handle_button_press(call:CallbackQuery):
    user_id=call.from_user.id
    bot.send_message(chat_id=call.message.chat.id,text=f"اسم گروه شما چیست؟ \n حداکثر {max_len_name} کاراکتر")
    bot.set_state(user_id=call.message.chat.id,state=banner_state.name,chat_id=call.message.chat.id)

     
#?##############################################
# make reserve
@bot.callback_query_handler(func=lambda call: call.data.startswith("get_banner_"))
def get_banner_from_user(call:CallbackQuery):
    user_id=call.from_user.id
    day=int(call.data.split('_')[2]) # it is a number in range(0 to 6)
    time_index=int(call.data.split('_')[3]) # its number , use 'time_of_day[time]'
    price= price_1 if time_index <5 else price_2 if 5<=time_index< 21 else price_3
    call_text=call.message.text
    text=call_text
    bot.edit_message_text(text=text,chat_id=call.message.chat.id,message_id=call.message.message_id)
    bot.send_message(text=msg_pls_send_banner,chat_id=call.message.chat.id)

    bot.set_state(user_id=call.message.chat.id,state=banner_state.banner,chat_id=call.message.chat.id)

    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['day'] = day
        data['date'] = cal_date(day)
        data['time'] = time_index
        data['price'] = price
#################
#get banner
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
    if  not is_banner_ok(banner=banner):
        bot.send_message(msg.from_user.id,text=msg_banner_not_mach)
        return False
    
    link=extract_link(banner)
    is_duplicate=is_duplicate_link(link=link,date=date)
    if is_duplicate:
        bot.send_message(chat_id=msg.from_user.id,text=msg_link_isDuplicated)
        return False
    
    print('test')
    #? check time and day 
    currentDateTime=get_current_datetime()
    banner_DateTime=f"{date} {dayClockArray[time_index]}:00"

    timeIsPast=compare_dates(time1=banner_DateTime,time2=currentDateTime)
    if timeIsPast:
        bot.send_message(chat_id=user_id,text=msg_time_is_past)
        return False
    #? end 
    make_reserve_transaction(user_id=user_id,price=price,time_index=time_index,date=date,banner=banner,link=link)
    if banner_need_approve:
        markup=InlineKeyboardMarkup()
        btn1=InlineKeyboardButton(text="تایید",callback_data="banner_accept")
        btn2=InlineKeyboardButton(text="رد کردن",callback_data="banner_deny")
        btn3=InlineKeyboardButton(text="تغییر بنر",callback_data="banner_custom")
        markup.add(btn1,btn2)
        markup.add(btn3)
        forwarded_msg=bot.forward_message(chat_id=ADMIN_ID_LIST[0],from_chat_id=msg.chat.id,message_id=msg.message_id)
        reserve_id=int(get_id_with_time_date_reserve(time=dayClockArray[time_index],date=date)[0])
        text=make_banner_acc_msg_to_admin(username=username,user_id=user_id,time=time_index,day=day,price=price,reserve_id=reserve_id[0])
        bot.send_message(chat_id=ADMIN_ID_LIST[0],text=text,reply_markup=markup,reply_to_message_id=forwarded_msg.message_id)
        bot.send_message(chat_id=msg.from_user.id,text=forward_banner_text)
    else:
        #todo problem
        result=get_id_with_time_date_reserve(time=dayClockArray[time_index],date=date)[0]
        reserve_id=int(result)
        transactions_admin_accept_banner(user_id=user_id,time_index=time_index,reserve_id=reserve_id,date=date)
        bot.send_message(chat_id=user_id,text=msg_banner_is_accepted) 


###
#deny btn 
@bot.callback_query_handler(func= lambda m:m.data =="banner_deny")
def admin_deny(call :CallbackQuery):
    info=call.message.text
    user_id=(find_pattern_id(info))
    reserve_id=get_reserve_id(info)
    DATA=parse_text_for_acc_admin_banner(info)
    time_index=int(DATA['time'])
    date=DATA['date']
    price=int(DATA['price'])
    try:
        admin_deny_banner(user_id=user_id,price=price,time_index=time_index,date=date,reserve_id=reserve_id)
    except Error as e:
        logging.error(f"error 'admin_deny' banner:  {e} ")
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"مشکلی پیش امد دوباره تلاش کنید \n {make_line} \n{text}")
    text=call.message.text
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text="این رزرو رد شد",callback_data="!?!?!?!")
    btn2=InlineKeyboardButton(text="علت رد کردن رزرو را بنویسید",callback_data=f"deny_message_to_{user_id}")
    markup.add(btn)
    markup.add(btn2)
    bot.send_message(chat_id=user_id,text=f"رزرو شما از سمت ادمین رد شد \n درصورت نیاز میتوانید با استفاده از دکمه '{btn_support}' با ادمین ارتباط برقرار کنید")
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)

#######
#accept reserve btn
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
        transactions_admin_accept_banner(user_id=user_id,time_index=time_index,reserve_id=reserve_id,date=date)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f"{info_text} \n {make_line} \n بنر تایید شد",reply_markup=markup)
        bot.send_message(chat_id=user_id,text=msg_banner_is_accepted) 
    except Error as e:
        logging.error(f" Error admin_accept_banner_btn: {e} ")
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
    #  bot.send_message(text=f"در یک خط اگر توضیحاتی لازم است برای گروه خود بنویسید \n حداکثر {max_len_des} کاراکتر",chat_id=msg.chat.id)
     bot.send_message(text="لینک خصوصی گروه خود را ارسال کنید",chat_id=msg.chat.id)

     bot.set_state(state=banner_state.link,user_id=msg.chat.id,chat_id=msg.chat.id)

#################
@bot.message_handler(state =banner_state.link)
def make_banner(msg : Message):
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
       data['link']=msg.text
       name=f"{data['name']}"
       member=f"{data['member']}"
       # description=f"{data['description']}"
       link=f"{data['link']}"
       #todo check link
    result =is_telegram_group_link(link=link)
    if not result:
        text=' لیک ارشال شده قابل قبول نیست \nلینک شما حتما باید خصوصی باشد و مربوط به گروه تلگرامی باشد\n لطفا مجدد تلاش کنید '
        bot.send_message(text=text,chat_id=msg.chat.id)
        return False;

    banner= make_channel_banner(name=name,members=member,link=link)
    bot.send_message(text="بنر شما اماده است",chat_id=msg.chat.id,)
    bot.send_message(text=banner,chat_id=msg.chat.id)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

########################################################################
#* convert scores
@bot.message_handler(func=lambda m:m.text == btn_convert_score)
def convert_score(msg: Message):
    user_id=int(msg.from_user.id)
    user_score=get_user_score(user_id)
    user_score_convert_able=divide_by_ten_mul_ten(user_score)
    user_score_converted=convert_scoreToValue(score=user_score_convert_able)
    if user_score_convert_able == 0 :
        btn = InlineKeyboardButton(text="امتیاز کافی ندارید", callback_data="!@!@!@!@!")
    else :
        btn =InlineKeyboardButton(text="تبدیل تمام امتیاز",callback_data=f"convertScore_{user_id}")
    
    markup=InlineKeyboardMarkup()
    markup.add(btn)
    text=f"{msg_change_score} \n {make_line} \n {make_change_score_text(score=user_score,convert_able=user_score_convert_able,value=user_score_converted)}"
    bot.send_message(chat_id=user_id,text=text,reply_markup=markup)

@bot.callback_query_handler(func= lambda m:m.data.startswith("convertScore_"))
def convert_scores(call:CallbackQuery):
    user_id=int(call.data.split('_')[1])
    user_score=get_user_score(user_id)
    score_to_change=divide_by_ten_mul_ten(user_score)
    value=convert_scoreToValue(score=score_to_change)
    db_convert_score(user_id=user_id,score_to_decrease=score_to_change,balance_to_increase=value)
    text=msg_score_is_converted
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)

 
##########################
#* see reserve users 
# #todo: have problem
@bot.message_handler(func=lambda m:m.text == markup_user_find_reserve)
def admin_btn_reserve(msg : Message):
    if  not bot_is_enable:
         send_bot_is_disable_text_to_user(user_id=msg.from_user.id) 
         return

    markup=InlineKeyboardMarkup()
    user_id=int(msg.from_user.id)
    is_not_any_reserve=True
    for i in range(-1,7):
        date=cal_date(i)
        reserve_id=get_id_with_user_id_date_reserve(user_id=user_id,date=date)
        if reserve_id is not None:
            is_any=False
            reserve_id=int(reserve_id[0])
            time = str(get_info_with_reserve_id(reserve_id)[3])[:5]
            btn=InlineKeyboardButton(text=f"{cal_day(i)} : {time}, {gregorian_to_jalali(date)}",callback_data=f"user_reserveID_{reserve_id}")
            markup.add(btn)
    if is_not_any_reserve:
            btn=InlineKeyboardButton(text=f"شما هیچ لینک رزور شده ای ندارید",callback_data=f"!!!!!!!")
            markup.add(btn)

    temp_date=get_current_date()
    text=f'برای مشاهده رزرو های خود روز مد نظر خود را انتخاب کنید\nامروز:  {cal_day(0)} , {gregorian_to_jalali(temp_date)} \n {make_line}'
    bot.send_message(chat_id=msg.from_user.id,text=text,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("user_reserveID_"))
def handle_button_press(call :CallbackQuery):
    reserve_id=int(call.data.split('_')[2])
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=admin_btn_cancel_reserve,callback_data=f"{admin_btn_cancel_reserve}_{reserve_id}")
    btn2=InlineKeyboardButton(text=admin_btn_change_banner,callback_data=f"{admin_btn_change_banner}_{reserve_id}")
    markup.add(btn1,btn2)
    text=get_banner_with_id_reserve(reserve_id=reserve_id)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)



#!#######################################################################
#* admin part  

# /admin
@bot.message_handler(commands=['admin'])
def start(msg : Message):
        if check_is_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text="خوش امدی ادمین",reply_markup=markup_main_admin)
        else:
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_user_main)
##########################
@bot.callback_query_handler(func= lambda m:m.data ==("change_bot_enable_disable"))
def convertUserID(call:CallbackQuery):
    value= "0" if bot_is_enable else "1"
    db_info_updateValue(name="bot_is_enable",newValue=value)
    toggle_bot_status()
    bot_status =['غیرفعال ❌','فعال ✅']
    text=f'ربات برای کاربران عادی {bot_status[int(value)]} شد'
    markup = markup_bot_setting(bot_is_enable=bot_is_enable)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=text , reply_markup=markup)
#########################
def toggle_bot_status():
    global bot_is_enable
    bot_is_enable = not bot_is_enable
##########################
#* user list
@bot.message_handler(func=lambda m:m.text == admin_btn_user_list)
def user_list(msg : Message):
     if not check_is_admin(msg.from_user.id):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_user_main)
            return False
     users=get_all_users()
     markup = create_pagination(users, 0)
     bot.send_message(chat_id=msg.chat.id,text=msg_userList,reply_markup=markup)

###########
@bot.callback_query_handler(func=lambda call: call.data.startswith(('prev', 'next')))
def paginate(call):
    page = int(call.data.split('_')[1])
    users=get_all_users()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_pagination(users, page))
###########
@bot.callback_query_handler(func=lambda call: call.data.startswith("users_"))
def handle_button_press(call :CallbackQuery):
    if not check_is_admin(int(call.from_user.id)):
            bot.send_message(call.message.chat.id,text=not_admin_text,reply_markup=markup_user_main)
            return False
    user_id=int(call.data.split('_')[1])
    username=get_username(user_id=user_id)
    balance=get_user_balance(user_id=user_id)
    score=get_user_score(user_id=user_id)
    text=f"id: {user_id}\n{make_user_info(user_id=user_id,balance=balance,score=score,username=username)}"

    markup=markup_make_admin_user_info()

    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)

##########################
#* restart_msg
@bot.callback_query_handler(func=lambda call: call.data== admin_btn_restart_bot)
def restart(call : CallbackQuery):
    text=msg_bot_need_reboot
    markup=ReplyKeyboardMarkup()
    markup.add("/start")
    users=get_all_users()
    for user in users:
        bot.send_message(user[0],text=text,reply_markup=markup)
##########################
#* find user
@bot.message_handler(func=lambda m:m.text == admin_btn_find_user_info)
def find_user(msg : Message):
    admin_id=msg.from_user.id
    bot.send_message(admin_id,"user_id کاربر مد نظر را ارسال کنید")
    bot.set_state(user_id=msg.from_user.id,state=admin_state.find_user,chat_id=msg.chat.id)
####
@bot.message_handler(state=admin_state.find_user)
def get_user_info_admin(msg:Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    user_id = convert_to_english_number(msg.text)
    result=user_exist(user_id=user_id)
    if not result:
        bot.send_message(chat_id=msg.from_user.id,text='کاربر در ربات وجود ندارد')
        return False
    user_id=int(msg.text)
    balance=get_user_balance(user_id)
    score=get_user_score(user_id)
    username=get_username(user_id=user_id)
    text=f"id: {user_id}\n{make_user_info(user_id=user_id,balance=balance,score=score,username=username)}"
    markup=markup_make_admin_user_info()
    bot.send_message(chat_id=msg.chat.id,text=text, reply_markup=markup)
############3
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
        logging.error(f"error delete a user: {e}")
        bot.send_message(call.message.from_user.id,text="مجدد تلاش کنید کاربر پاک نشد")

##########################
#* bot setting
@bot.message_handler(func=lambda m:m.text == admin_btn_bot_setting)
def bot_info(msg : Message):
    if not check_is_admin(msg.from_user.id):
           bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_user_main)
           return False
    count_users=get_users_count()[0]
    text=f"""تعداد کل کاربر های ربات : {count_users}
    سازنده ربات : <a href='tg://user?id={ADMIN_ID_LIST[0]}'>{creator_username}</a>"""
    markup=markup_bot_setting(bot_is_enable=bot_is_enable)
    bot.send_message(msg.from_user.id,text=text,reply_markup=markup)
#######
@bot.callback_query_handler(func=lambda call: call.data== admin_btn_bot_info_change_cart)
def handle_button_press(call :CallbackQuery):
    user_id=call.from_user.id
    text=f"اطلاعت فعلی کارت \n{get_cart_info()}"
    bot.send_message(user_id,text=text)
    bot.send_message(user_id,text="شماره کارت را وارد کنید")
    bot.set_state(user_id=call.message.chat.id,state=admin_state.change_cart_number,chat_id=call.message.chat.id)
#####
@bot.message_handler(state= admin_state.change_cart_number)
def msg_to_all(msg : Message):
    text=msg.text
    user_id=msg.from_user.id

    if not text_is_cart_number(text):
        bot.send_message(user_id,"شماره کارت وارد شده صحیح نسیت دوباره تلاش کنید")
        return False
    bot.send_message(user_id,"نام مالک کارت را وارد کنید")
    bot.set_state(user_id=msg.from_user.id,state=admin_state.change_cart_name,chat_id=msg.chat.id)
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['CART_NUMBER']=text

@bot.message_handler(state= admin_state.change_cart_name)
def msg_to_all(msg : Message):
    text=msg.text
    user_id=msg.from_user.id
    bot.send_message(user_id,"نام بانک را وارد کنید")
    bot.set_state(user_id=msg.from_user.id,state=admin_state.change_cart_bank_name,chat_id=msg.chat.id)
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['CART_NAME']=text

@bot.message_handler(state= admin_state.change_cart_bank_name)
def msg_to_all(msg : Message):
    text=msg.text
    user_id=msg.from_user.id
    with bot.retrieve_data(msg.from_user.id,msg.chat.id) as data :
        data['CART_BANK']=text
        CART_BANK=str(data['CART_BANK'])
        CART_NUMBER=str(data['CART_NUMBER'])
        CART_NAME=str(data['CART_NAME'])
    db_set_new_cart(bank_name=CART_BANK,number=CART_NUMBER,owner=CART_NAME)
    text=f"اطلاعات کارت تغییر کرد \n{make_line}\n {get_cart_info()}"
    bot.send_message(user_id,text)
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)

##########################
#?send msg to all
@bot.message_handler(func=lambda m:m.text == admin_btn_send_msg_to_all)
def msg_to_all(msg : Message):
    if not check_is_admin(int(msg.from_user.id)):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_user_main)
            return False
    bot.send_message(msg.chat.id,text="پیامی برای ارسال به همه برای من بنویسید")
    bot.set_state(user_id=msg.from_user.id,state=admin_state.message_to_all,chat_id=msg.chat.id)

######
    
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
#* see reserve admin
@bot.message_handler(func=lambda m:m.text == admin_btn_reserves)
def admin_btn_reserve(msg : Message):
    markup=InlineKeyboardMarkup()
    btn=InlineKeyboardButton(text=f"{cal_day(-1)} : {gregorian_to_jalali(cal_date(-1))}",callback_data=f"admin_time_btn_-1")
    markup.add(btn)
    for i in range(7):
        btn=InlineKeyboardButton(text=f"{cal_day(i)} : {gregorian_to_jalali(cal_date(i))}",callback_data=f"admin_time_btn_{i}")
        markup.add(btn)
    temp_date=get_current_date()
    text=f'برای مشاهده رزرو ها روز مد نظر خود را انتخاب کنید\nامروز:  {cal_day(0)}\n{temp_date} , {gregorian_to_jalali(temp_date)} \n {make_line}'
    bot.send_message(chat_id=msg.from_user.id,text=text,reply_markup=markup)
#########3
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_time_btn_"))
def handle_button_press(call :CallbackQuery):
    date_index=int(call.data.split('_')[3])
    user_id=call.from_user.id
    date=cal_date(date_index)
    markup=InlineKeyboardMarkup()
    for  time in dayClockArray:
        reserve_id= get_id_with_time_date_reserve(date=date,time=time)
        if reserve_id is not None :
            reserve_id=reserve_id[0]
            approved =is_reserve_approved(reserve_id)
            if approved != 0:
                text=f'id: {get_id_reserver_channel_timing(date=date,time=time)[0]}-time: {time}'
                btn=InlineKeyboardButton(text=text,callback_data=f"admin_reserveId_{reserve_id}")
                markup.add(btn)
    text=f'day:{cal_day(date_index)}\ndate : {date}  '
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_reserveId_"))
def handle_button_press(call :CallbackQuery):
    reserve_id=int(call.data.split('_')[2])
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=admin_btn_cancel_reserve,callback_data=f"{admin_btn_cancel_reserve}_{reserve_id}")
    btn2=InlineKeyboardButton(text=admin_btn_change_banner,callback_data=f"{admin_btn_change_banner}_{reserve_id}")
    markup.add(btn1,btn2)
    text=get_banner_with_id_reserve(reserve_id=reserve_id)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)

#cancel banner

@bot.callback_query_handler(func=lambda call: call.data.startswith(admin_btn_cancel_reserve))
def handle_button_press(call :CallbackQuery):
    reserve_id=int(call.data.split('_')[1])
    try:
        DATA=get_info_with_reserve_id(reserve_id=reserve_id)
        user_id=int(DATA[0])
        price=int(DATA[1])
        date=DATA[2]
        time_index=DATA[4]
        reserve_time=dayClockArray[time_index]        
        #*  check time
        current_dateTime=get_current_datetime()
        banner_dateTime=f"{date} {dayClockArray[time_index]}:00"
        
        cancel_able=compare_dates(time1=current_dateTime,time2=banner_dateTime)

        if not cancel_able:
            bot.send_message(call.message.chat.id,text=msg_to_late_to_cancel)
            return False
        #* end check time
        admin_deny_banner(user_id=user_id,price=price,time_index=time_index,date=date,reserve_id=reserve_id)
        markup=InlineKeyboardMarkup()
        btn1=InlineKeyboardButton(text='این رزرو کنسل شد',callback_data=f"!!!!!!!!!!!!!")
        markup.add(btn1)
        text=call.message.text
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)
    except Error as e:
        logging.error(e)
        bot.send_message(chat_id=call.from_user.id,text="دوباره تلاش کنید")

@bot.callback_query_handler(func=lambda call: call.data.startswith(admin_btn_change_banner))
def handle_button_press(call :CallbackQuery):
    reserve_id=int(call.data.split('_')[1])
    bot.send_message(chat_id=call.from_user.id,text="بنر جدید را ارسال کنید")
    bot.set_state(user_id=call.message.chat.id,state=admin_state.change_banner,chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['reserve_id'] =reserve_id


@bot.message_handler(state=admin_state.change_banner)
def handle_non_photo(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        reserve_id= data['reserve_id'] 
    banner=msg.text
    if is_banner_ok(banner=banner):
        bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
        try:
            result =change_banner_reserve(reserve_id=reserve_id,banner=banner)
            if result :
                bot.send_message(chat_id=msg.from_user.id,text="بنر تغییر کرد")
            else:
                bot.send_message(chat_id=msg.from_user.id,text="دوباره تلاش کنید")

        except Error as e :
            print(e)
    else:
        bot.send_message(chat_id=msg.from_user.id,text="بنر با الگوی کانال همخوانی ندارد")
        
##########################
#?check income
@bot.message_handler(func=lambda m:m.text == admin_btn_check_income)
def msg_to_all(msg : Message):
     if not check_is_admin(int(msg.from_user.id)):
            bot.send_message(chat_id=msg.chat.id,text=not_admin_text,reply_markup=markup_user_main)
            return False
     markup=InlineKeyboardMarkup(row_width=3)
     buttons = []
     for index,month in enumerate(months, start=1):
          btn=InlineKeyboardButton(text=f"{index}: {month}",callback_data=f"month_{index}")
          buttons.append(btn)
     for i in range(0, len(buttons), 3):
          markup.row(*buttons[i:i+3])
     bot.send_message(msg.chat.id,text=msg_check_income,reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("month_"))
def handle_button_press(call :CallbackQuery):
    month=(call.data.split('_')[1])
    text="❔ کدام نوع تراکنش ❔"
    markup=InlineKeyboardMarkup(row_width=2)
    btn1=InlineKeyboardButton(text="تراکنش های تایید شده",callback_data=f"income_approved_{month}")
    btn2=InlineKeyboardButton(text="تمام تراکنش ها",callback_data=f"income_all_{month}")
    markup.add(btn1,btn2)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, reply_markup=markup)
#########3
@bot.callback_query_handler(func=lambda call: call.data.startswith("income_approved_"))
def handle_button_press(call :CallbackQuery):

    month=int(call.data.split('_')[2])
    income=get_transactions_of_month_approved_income(year="2024",month=f"{month}")
    text=msg_create_income_info(income,month)
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )

@bot.callback_query_handler(func=lambda call: call.data.startswith("income_all_"))
def handle_button_press(call :CallbackQuery):
    month=int(call.data.split('_')[2])
    income=get_transactions_of_month_income(year="2024",month=f"{month}")
    text=msg_create_income_info(income,month)
    
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text, )
##########################################################################################################
@bot.callback_query_handler(func=lambda call: call.data == admin_btn_increase_balance)
def handle_button_press(call :CallbackQuery):
    msg_text=call.message.text
    text=f'{msg_text}\n {make_line} \n مبلغ مورد نظر را وارد کنید ،افزایش موجودی کاربر' 
    bot.send_message(chat_id=call.from_user.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_state.increase_balance,chat_id=call.message.chat.id)
    user_id=find_pattern_id(msg_text)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id

@bot.callback_query_handler(func=lambda call: call.data == admin_btn_decrease_balance)
def handle_button_press(call :CallbackQuery):
    msg_text=call.message.text
    text=f'{msg_text}\n {make_line} \n مبلغ مورد نظر را وارد کنید کاهش موجودی کاربر'
    bot.send_message(chat_id=call.from_user.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_state.decrease_balance,chat_id=call.message.chat.id)
    user_id=find_pattern_id(msg_text)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id

@bot.callback_query_handler(func=lambda call: call.data == admin_btn_increase_score)
def handle_button_press(call :CallbackQuery):
    msg_text=call.message.text
    text=f'{msg_text}\n {make_line} \n میزان مورد نظر را وارد کنید، افزایش امتیاز کاربر'
    bot.send_message(chat_id=call.from_user.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_state.increase_score,chat_id=call.message.chat.id)
    user_id=find_pattern_id(msg_text)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id

@bot.callback_query_handler(func=lambda call: call.data == admin_btn_decrease_score)
def handle_button_press(call :CallbackQuery):
    msg_text=call.message.text
    text=f'{msg_text}\n {make_line} \n میزان مورد نظر را وارد کنید، کاهش امتیاز کاربر'
    bot.send_message(chat_id=call.from_user.id,text=text)
    bot.set_state(user_id=call.message.chat.id,state=admin_state.decrease_score,chat_id=call.message.chat.id)
    user_id=find_pattern_id(msg_text)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['user_id'] = user_id

####################################################################################
@bot.message_handler(state=admin_state.increase_balance)
def handle_non_photo(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id= data['user_id'] 
    number=msg.text
    amount= int(convert_to_english_number(number))
    before=get_user_balance(user_id)
    increase_balance(user_id=user_id,increase_amount=amount)
    after=get_user_balance(user_id)
    text=f'تغییرات لازم انجام شد \n before: {before} \n after:{after}'
    bot.send_message(chat_id=msg.from_user.id,text=text)
###########
@bot.message_handler(state=admin_state.decrease_balance)
def handle_non_photo(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id= data['user_id'] 
    number=msg.text
    amount= int(convert_to_english_number(number))
    before=get_user_balance(user_id)
    result =decrease_balance(user_id=user_id,decrease_balance_amount=amount)
    if not result:
        bot.send_message(chat_id=msg.from_user.id,text="موجودی کاربر کمتر از انتخاب شماست")
        return
    after=get_user_balance(user_id)
    text=f'تغییرات لازم انجام شد \n before: {before} \n after:{after}'
    bot.send_message(chat_id=msg.from_user.id,text=text)
###########
@bot.message_handler(state=admin_state.increase_score)
def handle_non_photo(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id= data['user_id'] 
    number=msg.text
    amount= int(convert_to_english_number(number))
    before=get_user_score(user_id)
    increase_score(user_id=user_id,increase_amount=amount)
    after=get_user_score(user_id)
    text=f'تغییرات لازم انجام شد \n before: {before} \n after:{after}'
    bot.send_message(chat_id=msg.from_user.id,text=text)
###########
@bot.message_handler(state=admin_state.decrease_score)
def handle_non_photo(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id= data['user_id'] 
    number=msg.text
    amount= int(convert_to_english_number(number))
    before=get_user_score(user_id)
    result=decrease_score(user_id=user_id,decrease_amount=amount)
    if not result:
        bot.send_message(chat_id=msg.from_user.id,text="موجودی کاربر کمتر از انتخاب شماست")
        return False
    after=get_user_score(user_id)
    text=f'تغییرات لازم انجام شد \n before: {before} \n after:{after}'
    bot.send_message(chat_id=msg.from_user.id,text=text)


##########################
#! error handler
# بخش دریافت رسید از کاربر
@bot.message_handler(state=user_state.pic_receipt, content_types=['text', 'video', 'document', 'audio', 'sticker', 'voice', 'location', 'contact'])
def handle_non_photo(msg: Message):
    # پیام خطا برای ارسال محتوای غیر از عکس
    bot.send_message(msg.chat.id, "لطفاً فقط یک عکس از رسید خود ارسال کنید.")

#!#########################
#any message from users
@bot.message_handler(func=lambda message: True)
def handle_non_photo(msg: Message):
    bot.send_message(msg.chat.id, "\n /start لطفا برای استفاده از ربات یا از دکمه های ربات استفاده کنید یا مجدد ربات را راه اندازی کنید")

########################################
def send_scheduled_message():
    #set time
    time=datetime.now().strftime('%H:%M')

    # set date
    if compare_time("00:00",add_time(initial_time=time,duration="00:01")) and compare_time(time,"02:15"):
        date=cal_date(-1)
    else:
        date=get_current_date()

    user_id=get_id_reserver_channel_timing(time=time,date=date)
    if user_id is not None :
        user_id=int(user_id[0])
        if user_id != 1 :
            reserve_id=get_id_with_time_date_reserve(time=time,date=date)[0]
            banner=get_banner_with_id_reserve(reserve_id)[0]
            for channel in CHANNELS_USERNAME:
                bot.send_message(chat_id=channel,text=banner,disable_web_page_preview=True,link_preview_options=False)
                bot.send_message(ADMIN_ID_LIST[0],text="یک بنر ارسال شد",disable_notification=disable_notification)
            
 
########################################
#* restart  msg
def startMessageToAdmin(enable=True,disable_notification=disable_notification):
    if not enable:
        return False

    text=f'{msg_restart} \n 🚫{get_current_datetime()}🚫'

    #get last log    
    latest_log_file = get_latest_log_file()

    for admin in ADMIN_ID_LIST:#send for all admins
        if latest_log_file:
            last_3_errors=get_last_errors(latest_log_file)
            error_message = "\n".join(last_3_errors)
            with open(latest_log_file, 'rb') as log_file:
                bot.send_document(admin, log_file,caption=f"{text}\n{error_message}",disable_notification=disable_notification)
            logging.info(f"send last log to admin [{admin}] : {latest_log_file}")
        else:
            logging.info("هیچ فایل لاگی پیدا نشد.")
            bot.send_message(chat_id=admin,text=f"{text}\n ⛔️فایل log وجود ندارد⛔️",disable_notification=disable_notification)  
#################################
def send_bot_is_disable_text_to_user(user_id):
    bot.send_message(chat_id=user_id,text=text_bot_is_disable)
#*#######################################################################################################
if __name__ == "__main__":
    try:
        #log init
        log_filename = f"./logs/output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        
        logging.basicConfig(filename=log_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.info("bot is Started")

        remove_old_logs()
        bot_is_enable = True if db_info_getValue(name="bot_is_enable") == "1" else False
        
        #basic setting
        dbCreateDatabases() # DATA BASE

        start_scheduler() # auto send post 
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        banner_need_approve=bool(db_info_getValue(name="banner_need_approve"))
        
        #basic functions
        startMessageToAdmin() # hello message
        
        
        bot.polling() # keep bot running

    except Exception as e:
        logging.error(f"error in main : {e}")



#* todo : disable bot
#* todo : reorder all of code
#todo: move all info to db
#todo : change price
#todo : time check
#todo: check access to channels