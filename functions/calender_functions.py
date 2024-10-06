from datetime import datetime, timedelta
from convertdate import persian
from configs.basic_info import days_of_week_name
#########################################################
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
def add_date(date_str:str, days:int):
    # تبدیل رشته تاریخ به شیء datetime
    date = datetime.strptime(date_str, '%Y-%m-%d')
    # اضافه کردن تعداد روزهای مورد نظر
    new_date = date + timedelta(days=days)
    # تبدیل نتیجه به فرمت رشته ای
    return new_date.strftime('%Y-%m-%d')

#########################################################
def is_difference_less_than_15_minutes(date1_str, date2_str):
    # تبدیل رشته‌ها به اشیاء datetime
    format_str = "%Y-%m-%d %H:%M:%S"
    date1 = datetime.strptime(date1_str, format_str)
    date2 = datetime.strptime(date2_str, format_str)
    
    # محاسبه‌ی تفاوت زمانی
    time_difference = abs(date1 - date2)
    
    # بررسی اینکه آیا اختلاف کمتر از ۱۵ دقیقه است
    return time_difference <= timedelta(minutes=15)
#########################################################
def compare_time(lower,than):
    """return true if time1 < time2"""
    time_format = "%H:%M"
    time_A = datetime.strptime(lower, time_format).time()
    time_B = datetime.strptime(than, time_format).time()
    if time_A<time_B :
        return True
    else:
        return False
#########################################################
def compare_dates(time1: str, time2: str, add_minutes: int = 30) -> bool:
    # تبدیل رشته‌های ورودی به شیء datetime
    format_str = "%Y-%m-%d %H:%M:%S"  # فرمت تاریخ و زمان
    datetime1 = datetime.strptime(time1, format_str)
    datetime2 = datetime.strptime(time2, format_str)

    # اگر ورودی سوم (دقیقه) داده شده باشد، به datetime1 اضافه شود
    if add_minutes is not None:
        datetime1 += timedelta(minutes=add_minutes)

    # مقایسه تاریخ‌ها و زمان‌ها
    return datetime1 < datetime2

#########################################################
def get_next_day(date_str):
    # تبدیل رشته تاریخ به شیء datetime
    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date_str, date_format)
    
    # اضافه کردن یک روز به تاریخ
    next_day = date_obj + timedelta(days=1)
    
    # تبدیل تاریخ جدید به رشته با فرمت اولیه
    return next_day.strftime(date_format)

#########################################################
def compare_date(lower_eq,than):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(lower_eq, time_format).date()
    time_B = datetime.strptime(than, time_format).date()
    if time_A<=time_B :
        return True
    else:
        return False
#########################################################
def compare_date_is_eq(date1,date2):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(date1, time_format).date()
    time_B = datetime.strptime(date2, time_format).date()
    if time_A==time_B :
        return True
    else:
        return False
#########################################################
def date_is_past(past,than):
    time_format = "%Y-%m-%d"
    time_A = datetime.strptime(past, time_format).date()
    time_B = datetime.strptime(than, time_format).date()
    if time_A<time_B :
        return True
    else:
        return False
#########################################################
def get_current_date():
    """ return : %Y-%m-%d """
    # دریافت تاریخ و ساعت لحظه‌ای
    now = datetime.now()
    # تبدیل به رشته با فرمت YYYY-MM-DD HH:MM:SS
    date_time_str = now.strftime("%Y-%m-%d")
    return date_time_str

#########################################################
def get_current_datetime():
    """ return : %Y-%m-%d %H:%M:%S """
    # دریافت تاریخ و ساعت لحظه‌ای
    now = datetime.now()
    # تبدیل به رشته با فرمت YYYY-MM-DD HH:MM:SS
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time_str
#########################################################
def cal_date(days):
    """make date of day
    get (-1 to 6 ) return like 2024-08-05 
    [-1 means yesterday ]
    [0 mean today ]
    [1 mean tomorrow]
    """
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

#########################################################
def cal_day(days):
    """get a number and return it day like
    1 => دوشنبه
    0 => یکشنبه"""
    tomorrow_date = datetime.now() + timedelta(days=days)
    tomorrow_weekday = tomorrow_date.weekday()
    tomorrow_persian = days_of_week_name[tomorrow_weekday]
    return tomorrow_persian

#########################################################
def get_current_time():
    """ return : %H:%M """

    # بدست آوردن زمان کنونی
    now = datetime.now()
    
    # قالب‌بندی زمان به صورت رشته‌ای با فرمت 'HH:MM:SS'
    current_time = now.strftime("%H:%M")
    
    return current_time
