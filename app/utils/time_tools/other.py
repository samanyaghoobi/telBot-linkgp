from datetime import datetime, timedelta

def get_weekday_farsi(index :int)->str:
    weekday_farsi = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"][index]
    return weekday_farsi


def is_more_than_30_minutes_left(target_time_str):
    now = datetime.now()
    today = datetime.today().date()

    try:
        # تبدیل رشته به datetime
        target_time = datetime.strptime(target_time_str, "%H:%M").time()
        target_datetime = datetime.combine(today, target_time)

        # فاصله زمانی بین هدف و حالا
        delta = target_datetime - now

        # بررسی اینکه آیا بیش از ۳۰ دقیقه مانده یا نه
        return delta > timedelta(minutes=30)
    except ValueError:
        # اگر فرمت ورودی اشتباه بود
        raise ValueError("زمان باید به فرمت HH:MM باشد")


def get_weekday_persian(date: datetime.date) -> str:
    weekdays_persian = {
        0: "دوشنبه",
        1: "سه‌شنبه",
        2: "چهارشنبه",
        3: "پنج‌شنبه",
        4: "جمعه",
        5: "شنبه",
        6: "یکشنبه",
    }
    
    # تبدیل weekday عددی به فارسی (0 = Monday)
    weekday_number = date.weekday()
    return weekdays_persian.get(weekday_number, "نامشخص")
