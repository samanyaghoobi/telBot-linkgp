from datetime import time
from database.repository.bot_setting_repository import BotSettingRepository
from database.session import SessionLocal

def get_price_from_db_for_time(input_time: str | time) -> int | None:
    """
    بررسی قیمت بر اساس ساعت ورودی با رجوع به تنظیمات دیتابیس
    """
    if isinstance(input_time, str):
        try:
            input_time = time.fromisoformat(input_time)
        except ValueError:
            return None  # فرمت نامعتبر مثل "25:90"

    db = SessionLocal()
    repo = BotSettingRepository(db)

    # تعریف بازه‌های زمانی کاری
    ranges = [
        ("13:00", "17:00", "price_1"),
        ("18:00", "23:59", "price_2"),
        ("00:00", "00:59", "price_2"),
        ("01:00", "02:00", "price_3"),
    ]

    for start_str, end_str, key in ranges:
        start = time.fromisoformat(start_str)
        end = time.fromisoformat(end_str)

        # بازه‌ای که از شب گذشته عبور می‌کند (مثلاً 00:00 تا 00:59)
        if start > end:
            in_range = input_time >= start or input_time <= end
        else:
            in_range = start <= input_time <= end

        if in_range:
            value = repo.bot_setting_get(key,default=50)
            try:
                return int(value)
            except ValueError:
                return None  # مقدار نادرست در دیتابیس

    return None  # خارج از ساعت کاری
