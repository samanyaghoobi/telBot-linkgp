from datetime import datetime, timedelta

from database.db_reserve import db_reserve_get_links_within_week_reserve
from database.db_timing import insert_channel_timing_for_custom_period
from functions.calender_functions import cal_date
date=cal_date(1)
test=insert_channel_timing_for_custom_period(start_date=date,duration=9)
# print(test)



def compare_dates(time1: str, time2: str, add_minutes: int = None) -> bool:
    # تبدیل رشته‌های ورودی به شیء datetime
    format_str = "%Y-%m-%d %H:%M:%S"  # فرمت تاریخ و زمان
    datetime1 = datetime.strptime(time1, format_str)
    datetime2 = datetime.strptime(time2, format_str)

    # اگر ورودی سوم (دقیقه) داده شده باشد، به datetime1 اضافه شود
    if add_minutes is not None:
        datetime1 += timedelta(minutes=add_minutes)

    # مقایسه تاریخ‌ها و زمان‌ها
    return datetime1 < datetime2

# مثال استفاده
time1 = "2024-02-01 12:29:00"
time2 = "2024-02-01 13:00:00"

result = compare_dates(time1, time2, 30)
print(result) 