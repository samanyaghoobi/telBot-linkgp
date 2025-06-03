from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,Message
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from app.utils.time_tools.covert_time_and_date import convertToPersianDateStr
from config import AVAILABLE_HOURS
from database.session import SessionLocal
from datetime import datetime, timedelta
from database.models.banner import Banner
from database.models.user import User
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository


@bot.callback_query_handler(func=lambda c: c.data.startswith("select_day_"))
def show_free_hours_for_day(call: CallbackQuery):
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
        markup.add(InlineKeyboardButton(get_message("msg.noFreeTime"), callback_data="none"))
    
    shamsi_date=convertToPersianDateStr(selected_date)
    bot.edit_message_text(
        text=f"⏰ ساعت های خالی برای  {shamsi_date}:",
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
    user :User= repo.get_user(call.from_user.id)

    # If user has no banners, notify them
    if not user or not user.banners:
        bot.answer_callback_query(call.id, get_message("msg.noBannerFind"))
        return

    # Prepare buttons to show user their banners
    markup = InlineKeyboardMarkup(row_width=1)
    for b in user.banners :
        if b : 
            banner:Banner=b
            if not banner.is_deleted:
                markup.add(InlineKeyboardButton(banner.title, callback_data=f"banner_{banner.id}_{selected_date}_{selected_hour}"))

    bot.edit_message_text(text=get_message("msg.selectBanner"),
                          chat_id=call.message.chat.id,message_id= call.message.id , reply_markup=markup)
