from telebot import  types
import mysql.connector # type: ignore
from datetime import datetime,timedelta
from configs.auth import ADMIN_ID_LIST, CHANNELS_USERNAME, DB_CONFIG
from configs.basic_info import *
from database.db_reserve import get_link_with_date_reserve
from database.db_transactions import get_all_transactions, get_transactions_of_month
from database.db_users import get_user_balance, get_username
from functions.calender_functions import cal_date, cal_day, gregorian_to_jalali
from main import  isMemberOf
from message_and_text.bot_messages import make_line
import re
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove

##############################################
def make_timing_of_day_msg(results,day,from_admin=False):
    time=[]
    date=gregorian_to_jalali(cal_date(day))
    for index in range(len(results)):
        if index !=0:
            if results[index] == 0:
                time.append("خالی")
            elif results[index]==1:
                time.append("درحال رزرو : منتظر تایید ادمین")
            else:
                if from_admin:
                    user_id=int(results[index])
                    time.append(f"""\nuser:<a href='tg://user?id={user_id}'>@{get_username(user_id=results[index])}</a>,<code>{user_id}</code>""")
                else:
                    time.append(f"رزرو شده است")

    text=f"""ساعت های خالی برای : <u>{cal_day(day)}</u> : 📆<u>{date}</u>📆
{make_line}
🩵طرح یک🩵
⏰حداقل یک ساعت پست اخر⏰
💵 قیمت = {price_1} هزارتومان💵
    13:00 ⬅️ {time[0]}
    14:00 ⬅️ {time[1]}
    15:00 ⬅️ {time[2]}
    16:00 ⬅️ {time[3]}
    17:00 ⬅️ {time[4]}
{make_line}
✨طرح دو ✨
⏰حداقل نیم ساعت پست اخر⏰
💵 قیمت = {price_2} هزارتومان💵
    18:00 ⬅️ {time[5]}
    18:30 ⬅️ {time[6]}
    19:00 ⬅️ {time[7]}
    19:30 ⬅️ {time[8]}
    20:00 ⬅️ {time[9]}
    20:30 ⬅️ {time[10]}
    21:00 ⬅️ {time[11]}
    21:30 ⬅️ {time[12]}
    22:00 ⬅️ {time[13]}
    22:30 ⬅️ {time[14]}
    23:00 ⬅️ {time[15]}
    23:30 ⬅️ {time[16]}
    00:00 ⬅️ {time[17]}
    00:30 ⬅️ {time[18]}
    01:00 ⬅️ {time[19]}
    01:30 ⬅️ {time[20]}
{make_line}
💎پست ویژه💎
💵 قیمت = {price_3} هزارتومان💵
⏰حداقل تا ساعت 13:00  پست اخر⏰
    02:00 ⬅️ {time[21]}
"""
    return text
###################################################
def divide_by_ten_mul_ten(number :int):
    return (number // 10)*10  # تقسیم صحیح
def convert_scoreToValue(score :int):
    return (score // 10 ) * base_score_value
###################################################
# تابعی برای ساخت صفحه‌بندی
def create_pagination(users_list, page, per_page=10):
    start = page * per_page
    end = start + per_page
    users_in_page = users_list[start:end]

    # ایجاد دکمه‌های شیشه‌ای برای کاربران
    keyboard = types.InlineKeyboardMarkup()
    for user in users_in_page:
        button = types.InlineKeyboardButton(f"{user[3]}:{user[0]}", callback_data=f"users_{user[0]}")
        keyboard.add(button)

    # دکمه‌های "قبلی" و "بعدی"
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton("⬅️ قبلی", callback_data=f'prev_{page-1}'))
    if end < len(users_list):
        nav_buttons.append(types.InlineKeyboardButton("➡️ بعدی", callback_data=f'next_{page+1}'))
    
    keyboard.row(*nav_buttons)
    
    return keyboard

###################################################
def make_reserve_info_text(time,date,day,price):
    return f"""مشخصات پیش فاکتور رزرو شما:
    روز = {day}
    تاریخ = {date} 
    ساعت = {time}
    قیمت = {price} هزار تومان
    """
def get_day_reserves(day):
    sql= f"SELECT * from channel_timing where record_date = '{cal_date(day)}'"
    with mysql.connector.connect(**DB_CONFIG) as connection:
          with connection.cursor()  as cursor:
            cursor.execute(sql)
            result =cursor.fetchone()
            return result
#################333
def check_is_admin(user_id : int):
     if user_id in ADMIN_ID_LIST:
          return True
     return False

#################3
def find_pattern_id(text):
    pattern = r"id: \d+"
    x=re.findall(pattern=pattern,string=text)[0].split()[1]
    return x



def find_pattern_balance_amount(text):
    pattern = r"balance increase amount:‌ \d+"
    x=re.findall(pattern=pattern,string=text)[0].split()[3]
    return x
def find_pattern_reserve(text):
    """[time,day,price]"""
    pattern = r"\d+"

    x=re.findall(pattern=pattern,string=text)
    return x

#####################
def make_channel_banner(name,members,link):
    banner=f"""Super GP

naмe : {name}

мeмвer: {members}

lιnĸ: {link}

@LinkGP"""
    return banner


def extract_link(banner):
    # الگوی regex برای پیدا کردن لینک
    # این الگو به دنبال رشته‌هایی می‌گردد که با http:// یا https:// شروع شده و پس از آن کاراکترهای معتبر URL قرار دارند
    pattern = r'https?://[^\s]+'
    
    # جستجوی الگو در متن
    match = re.search(pattern, banner)
    
    # اگر لینک پیدا شد، آن را برگردان
    if match:
        return match.group(0)
    else:
        return None



#########################################################
def get_total_income():
    reservations=get_all_transactions()
    amount=0;
    for reserve in reservations:
          amount=amount+reserve[2]
    return amount

#########################################################

def is_banner_ok(banner):
    regex = re.compile(default_banner_pattern, re.MULTILINE | re.VERBOSE)
    return bool(regex.match(banner))

#####################3
def make_banner_acc_msg_to_admin(user_id,username,time, day, price,reserve_id):
     text=f"""id: {user_id} 
username: @{username} 
user_balance: {get_user_balance(user_id=user_id)}
time: {time} = {dayClockArray[time]} 
day: {day} = {cal_day(day)} 
date: {cal_date(day)}
price: {price}
---------------
reserve_id: {reserve_id}
"""
     return text

######################3

def parse_text_for_acc_admin_banner(text):
    # Split the text into lines
    lines = text.splitlines()
    
    # Initialize a dictionary to hold the parsed data
    data = {}

    # Extract the required information from each line
    for line in lines:
        if line.startswith("username:"):
            data['username'] = line.split(":")[1].strip().replace('@', '')
        elif line.startswith("time:"):
            data['time'] = line.split(":")[1].strip().split('=')[0].strip()
        elif line.startswith("id:"):
            data['user_id'] = line.split(":")[1].strip().split('=')[0].strip()
        elif line.startswith("day:"):
            data['day'] = line.split(":")[1].strip().split('=')[0].strip()
        elif line.startswith("date:"):
            data['date'] = line.split(":")[1].strip().split('=')[0].strip()
        elif line.startswith("reserve_id:"):
            data['reserve_id'] = line.split(":")[1].strip().split('=')[0].strip()
        elif line.startswith("price:"):
            data['price'] = line.split(":")[1].strip().split('=')[0].strip()

    # Convert dictionary to JSON
    return data
#######
def convert_to_time(string):
    time_format = "%H:%M"
    
    # Convert the initial time string to a datetime object
    time = datetime.strptime(string, time_format).time()
    return time
#######

def get_reserve_id(text):
    # Split the text into lines
    lines = text.splitlines()
    

    # Extract the required information from each line
    for line in lines:
        if line.startswith("reserve_id:"):
            data = line.split(":")[1]

    # Convert dictionary to JSON
    return data

####join channels markup
def makeJoinChannelMarkup(user_id):
    markup=InlineKeyboardMarkup()
    channels = [item.replace('@', '') for item in CHANNELS_USERNAME]
    for index,channel in enumerate(CHANNELS_USERNAME,start=0):#make btn for plans
        if not isMemberOf(user_id=user_id,channel=channel):
            btn=InlineKeyboardButton(text=f"عضو شدن در {channels[index]}",url=f"https://t.me/{channels[index]}")
            markup.add(btn)
    button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
    markup.add(button)
    return markup
#######################
def find_index(item,list):
    try:
        index = list.index(item)
        return index
    except ValueError:
        return "Time not found in the list"
    

def convert_to_english_number(text):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    arabic_digits = "٠١٢٣٤٥٦٧٨٩"
    english_digits = "0123456789"
    
    translation_table = str.maketrans(persian_digits + arabic_digits, english_digits * 2)
    return (text.translate(translation_table))

def is_telegram_group_link(link):
    # تعریف الگوی regex برای شناسایی لینک گروه‌های تلگرام
    pattern = r'^(https?://)?(www\.)?(t\.me/joinchat/|t\.me/\+|telegram\.me/joinchat/|telegram\.me/\+).+'
    
    # بررسی اینکه آیا لینک با الگوی گروه تلگرام مطابقت دارد
    if re.match(pattern, link):
        return True
    else:
        return False

def is_duplicate_link(link,date):
    try:
        links=get_link_with_date_reserve(date)
        if links is None:
            return False
        for l in links:
            print(f"test : {link} : {l[0]}")
            if link == l[0]:
                return True
        return False
    except (KeyError,TypeError) as e:
        print (f"is_duplicate_link : {e}")
        return True