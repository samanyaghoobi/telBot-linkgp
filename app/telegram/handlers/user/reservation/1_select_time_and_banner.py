from app.utils.markup.week_markup import show_week_for_navigation
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,Message
from app.telegram.bot_instance import bot
from app.utils.messages import get_message
from database.base import SessionLocal
from datetime import datetime, timedelta

from database.models.banner import Banner
from database.models.user import User
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

# Constant: Fixed list of available reservation hours
#todo move to db 
AVAILABLE_HOURS = [
    "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "18:30",
    "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
    "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00", "01:30", "02:00"
]
# Step 2: Show available hours for the selected day
@bot.callback_query_handler(func=lambda c: c.data.startswith("select_day_"))
def show_free_hours_for_day(call: CallbackQuery):
    print(call.data)

    selected_date = call.data.replace("select_day_", "")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    db = SessionLocal()
    reserveRepo = ReservationRepository(db)
    settingRepo = BotSettingRepository(db)
    now = datetime.now()
    
    reserved_slots = reserveRepo.get_reservations_for_date(selected_date)
    reserved_times = {r.time for r in reserved_slots}

    TIME_INTERVAL_MINUTES = float(settingRepo.bot_setting_get("TIME_INTERVAL_MINUTES", "30"))

    markup = InlineKeyboardMarkup()
    any_available = False
    buttons = []

    for hour_str in AVAILABLE_HOURS:

        # hour_time = datetime.strptime(hour_str, "%H:%M").time()
        # if selected_date == now.date() and (hour_time + timedelta(minutes=TIME_INTERVAL_MINUTES)) <= now.time():
        #     continue
        hour_time = datetime.strptime(hour_str, "%H:%M").time()

        # اگر امروز است و زمان گذشته، رد کن
        if selected_date == now.date():
            end_time = (datetime.combine(now.date(), hour_time) + timedelta(minutes=TIME_INTERVAL_MINUTES)).time()
            if end_time <= now.time():
                continue
                
        if hour_time not in reserved_times:
            any_available = True
            icon = "🟢"
            btn_text = f"{icon} {hour_str}"
            callback = f"reserve_{selected_date}_{hour_str}"
            buttons.append(InlineKeyboardButton(btn_text, callback_data=callback))

    for i in range(0, len(buttons), 2):
        markup.row(*buttons[i:i+2])

    if not any_available:
        markup.add(InlineKeyboardButton("❌ هیچ ساعتی آزاد نیست", callback_data="none"))

    bot.edit_message_text(
        text=f"⏰ ساعت های خالی برای  {selected_date}:",
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda c: c.data.startswith("reserve_"))
def select_banner_for_reservation(call: CallbackQuery):
    # Extract the selected date and time
    selected_date, selected_hour = call.data.replace("reserve_", "").split("_")
    selected_date = datetime.strptime(selected_date,"%Y-%m-%d").date()
    selected_hour = selected_hour  # This is the hour chosen by the user

    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_user(call.from_user.id)

    # If user has no banners, notify them
    if not user or not user.banners:
        bot.answer_callback_query(call.id, "شما هیچ بنری ثبت نکرده‌اید.")
        return

    # Prepare buttons to show user their banners
    markup = InlineKeyboardMarkup(row_width=1)
    for banner in user.banners:
        markup.add(InlineKeyboardButton(banner.title, callback_data=f"banner_{banner.id}_{selected_date}_{selected_hour}"))

    bot.edit_message_text(text="📋 لطفاً بنری که می‌خواهید برای این زمان انتخاب کنید را انتخاب کنید.",
                          chat_id=call.message.chat.id,message_id= call.message.id , reply_markup=markup)
