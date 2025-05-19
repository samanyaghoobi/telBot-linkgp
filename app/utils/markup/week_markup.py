from datetime import date, timedelta
import jdatetime
from telebot import types 
from app.telegram.bot_instance import  bot
from app.utils.time_tools.weekday_farsi import get_weekday_farsi
from database.base import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository

def show_week_for_navigation(message:str, start_of_week)->types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=3)

    for i in range(7):
        date = start_of_week + timedelta(days=i)
        if date < date.today():
            continue
        day_shamsi = jdatetime.date.fromgregorian(date=date)
        weekday_farsi = get_weekday_farsi(date.weekday())
        label = f"{weekday_farsi} {day_shamsi.strftime('%d-%m-%Y')}"
        callback = f"select_day_{date.isoformat()}"
        markup.add(types.InlineKeyboardButton(label, callback_data=callback))

    if start_of_week > date.today():  # Prevent going back more than this week
        prev_week_callback = f"week_prev_{start_of_week.isoformat()}"
        markup.add(types.InlineKeyboardButton("⏪ هفته قبلی", callback_data=prev_week_callback))
    db = SessionLocal()
    setting_repo = BotSettingRepository(db)
    max_future_date = int(setting_repo.bot_setting_get("max_future_date", "32"))
    if start_of_week < date.today() + timedelta(days=max_future_date):
        next_week_callback = f"week_next_{start_of_week.isoformat()}"
        markup.add(types.InlineKeyboardButton("⏩ هفته بعدی", callback_data=next_week_callback))

    return markup

