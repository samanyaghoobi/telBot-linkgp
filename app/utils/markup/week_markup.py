from datetime import date, timedelta
import jdatetime
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from app.telegram.bot_instance import  bot
from app.utils.time_tools.covert_time_and_date import dateInPersian, date_to_persian
from app.utils.time_tools.other import get_weekday_farsi
from database.session import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository
from collections import defaultdict
from database.repository.reservation_repository import ReservationRepository

def show_week_for_navigation(message:str, start_of_week,input_markup:InlineKeyboardMarkup=None)-> InlineKeyboardMarkup:
    markup = input_markup or InlineKeyboardMarkup(row_width=3)

    for i in range(7):
        date_ = start_of_week + timedelta(days=i)
        if date_ < date.today():
            continue
        day_shamsi = jdatetime.date.fromgregorian(date=date_)
        weekday_farsi = get_weekday_farsi(date_.weekday())
        label = f"{weekday_farsi} {day_shamsi.strftime('%d-%m-%Y')}"
        callback = f"select_day_{date_.isoformat()}"
        markup.add(InlineKeyboardButton(label, callback_data=callback))

    if start_of_week > date.today():  # Prevent going back more than this week
        prev_week_callback = f"week_prev_{start_of_week.isoformat()}"
        markup.add(InlineKeyboardButton("⏪ هفته قبلی", callback_data=prev_week_callback))

    db = SessionLocal()
    try:
        setting_repo = BotSettingRepository(db)
        max_future_date = int(setting_repo.bot_setting_get("max_future_date", "32"))
    finally:
        db.close()

    if start_of_week < date.today() + timedelta(days=max_future_date):
        next_week_callback = f"week_next_{start_of_week.isoformat()}"
        markup.add(InlineKeyboardButton("⏩ هفته بعدی", callback_data=next_week_callback))

    return markup


def show_reservation_day_selector(start_date: date):
    db = SessionLocal()
    try:
        repo = ReservationRepository(db)
        end_date = start_date + timedelta(days=7)

        # 📦 فقط یک کوئری برای همه رزروهای هفته
        reservations = repo.get_reservations_between_dates(start_date, end_date)
    finally:
        db.close()

    # 🔢 شمارش تعداد رزرو به ازای هر روز
    count_by_day = defaultdict(int)
    for r in reservations:
        count_by_day[r.date] += 1

    markup = InlineKeyboardMarkup(row_width=2)

    for i in range(7):
        day = start_date + timedelta(days=i)
        persian = date_to_persian(day)
        count = count_by_day.get(day, 0)
        label = f"{persian} - {count} رزرو"
        markup.add(InlineKeyboardButton(label, callback_data=f"admin_reserve_day_{day.isoformat()}"))

    prev_week = start_date - timedelta(days=7)
    next_week = start_date + timedelta(days=7)
    markup.add(
        InlineKeyboardButton("⬅️ هفته قبل", callback_data=f"admin_reserve_all_dates_{prev_week.isoformat()}"),
        InlineKeyboardButton("➡️ هفته بعد", callback_data=f"admin_reserve_all_dates_{next_week.isoformat()}")
    )
    return markup
