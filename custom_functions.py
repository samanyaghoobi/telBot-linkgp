import mysql.connector # type: ignore
from config import ADMIN_ID_LIST, CHANNELS_USERNAME, DB_CONFIG,days_of_week,price_1,price_2,price_3,default_banner_pattern,time_of_day
from datetime import datetime,timedelta
from convertdate import persian
from db_connections import get_all_transactions, get_transactions_of_month, get_user_balance
from main import bot, isMemberOf, isMemberOfChannels
from bot_messages import make_line
import re
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery,ReplyKeyboardRemove

##############################################
def make_timing_of_day(results,day):
    time=[]
    for index in range(len(results)):
        if index !=0:
            if results[index] == 0:
                time.append("خالی")
            elif results[index]==1:
                time.append("درحال رزرو : منتظر تایید ادمین")
            else:
                time.append(f"رزرو شده است : {results[index]}")
    text=f"""اخرین بروز رسانی : \n{get_current_datetime()}
{make_line}
روز رزرو : {cal_day(day)}
🩵🩵🩵🩵🩵🩵🩵طرح یک🩵🩵🩵🩵🩵🩵
حداقل یک ساعت پست اخر
💵 قیمت = {price_1} هزارتومان
13:00 ⬅️ {time[0]}
14:00 ⬅️ {time[1]}
15:00 ⬅️ {time[2]}
16:00 ⬅️ {time[3]}
17:00 ⬅️ {time[4]}
{make_line}
✨✨✨✨✨✨✨طرح دو ✨✨✨✨✨✨
حداقل نیم ساعت پست اخر
💵 قیمت = {price_2} هزارتومان
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
💎💎💎💎💎💎💎پست ویژه💎💎💎💎💎💎
💵 قیمت = {price_3} هزارتومان
حداقل تا ساعت 13:00  پست اخر
02:00 ⬅️ {time[21]}
"""
    return text
###################################################

###################################################

def current_date():
     return datetime.now().strftime("%Y-%m-%d")

def cal_date(days):
    """make date of day
    get (-1 to 6 ) return like 2024-08-05
    -1 means yesterday 
    0 mean today 
    1 mean tomorrow
    """
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

def cal_day(days):
    """get a number and return it day like
    1 => دوشنبه
    0 => یکشنبه"""
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

def get_current_time():
    # بدست آوردن زمان کنونی
    now = datetime.now()
    
    # قالب‌بندی زمان به صورت رشته‌ای با فرمت 'HH:MM:SS'
    current_time = now.strftime("%H:%M")
    
    return current_time

###################################################
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
def check_admin(user_id):
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
def make_channel_banner(name,description,members,link):
    banner=f"""Super GP

naмe : {name}

мeмвer: {members}

𝓭𝓮𝓼𝓬𝓻𝓲𝓹𝓽𝓲𝓸𝓷: {description}

lιnĸ: {link}

@LinkGP"""
    return banner


def send_test_msg_to_admin():
    bot.send_message(chat_id=ADMIN_ID_LIST[1],text="this is test msg")


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
def get_total_income_approved():
    reservations=get_all_transactions()
    amount=0;
    for reserve in reservations:
          if(reserve[1] is  True):
            amount=amount+reserve[2]
    return amount
#########################################################
def get_month_income(year,month): 
    reservations=get_transactions_of_month(year=year,month=month)
    amount=0;
    for reserve in reservations:
            amount=amount+reserve[2]
    return amount
#########################################################
def get_month_income_approved(year,month):
    reservations=get_transactions_of_month(year=year,month=month)
    amount=0;
    for reserve in reservations:
          if(reserve[1] is True):
            amount=amount+reserve[2]
    return amount
#########################################################

def add_time(initial_time: str, duration: str) -> str:
    """
    Add a duration to a given time.

    Parameters:
    - initial_time (str): The initial time in "HH:MM" format.
    - duration (str): The duration to add in "HH:MM" format.

    Returns:
    - str: The new time in "HH:MM" format after adding the duration.
    """
    # Define the time format
    time_format = "%H:%M"
    
    # Convert the initial time string to a datetime object
    time_obj = datetime.strptime(initial_time, time_format)
    
    # Parse the duration string to extract hours and minutes
    hours, minutes = map(int, duration.split(":"))
    
    # Create a timedelta object for the duration
    time_delta = timedelta(hours=hours, minutes=minutes)
    
    # Add the timedelta to the initial time
    new_time = time_obj + time_delta
    
    # Format the new time as a string
    new_time_str = new_time.strftime(time_format)
    
    return new_time_str

#########################################################
def compare_time(time1,time2):
    """return true if time1 < time2"""
    time_format = "%H:%M"
    time_A = datetime.strptime(time1, time_format).time()
    time_B = datetime.strptime(time2, time_format).time()
    if time_A<time_B :
        return True
    else:
        return False
  #########################################################
def is_banner_ok(banner):
    # print(banner)
    regex = re.compile(default_banner_pattern, re.MULTILINE | re.VERBOSE)
    return bool(regex.match(banner))

#####################3
def make_banner_acc_msg_to_admin(user_id,username,time, day, price,reserve_id):
     text=f"""id: {user_id} 
username: @{username} 
user_balance: {get_user_balance(user_id=user_id)[0]}
time: {time} = {time_of_day[time]} 
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
            btn=InlineKeyboardButton(text=f"عضو شدن در @{channels[index]}",url=f"https://t.me/{channels[index]}")
            markup.add(btn)
    button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
    markup.add(button)
    return markup
    