import mysql.connector # type: ignore
from config import ADMIN_ID_LIST, DB_CONFIG,days_of_week
from datetime import datetime,timedelta
from convertdate import persian
from db_connections import get_all_reservations, get_reservations_of_month
from main import bot
import re
##############################################
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
###################################################
def make_user_info (username,user_id,balance,score):
     text=f""""اطلاعات حساب کاربری  :
نام کاربری : <a href='tg://user?id={user_id}'>{username}</a>
شناسه کاربری :<code>{user_id}</code>
موجودی : {balance}
امتیاز شما: {score}
"""
     return text
###################################################

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




#########################################################
def get_total_income():
    reservations=get_all_reservations()
    amount=0;
    for reserve in reservations:
          amount=amount+reserve[2]
    return amount
#########################################################
def get_total_income_approved():
    reservations=get_all_reservations()
    amount=0;
    for reserve in reservations:
          if(reserve[1] is  True):
            amount=amount+reserve[2]
    return amount
#########################################################
def get_month_income(year,month): 
    reservations=get_reservations_of_month(year=year,month=month)
    amount=0;
    for reserve in reservations:
            amount=amount+reserve[2]
    return amount
#########################################################
def get_month_income_approved(year,month):
    reservations=get_reservations_of_month(year=year,month=month)
    amount=0;
    for reserve in reservations:
          if(reserve[1] is True):
            amount=amount+reserve[2]
    return amount
