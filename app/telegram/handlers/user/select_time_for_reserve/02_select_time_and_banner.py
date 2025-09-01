from app.utils.markup.week_markup import show_week_for_navigation
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from app.utils.time_tools.covert_time_and_date import convertToPersianDateStr
from app.utils.time_tools.other import get_weekday_persian, is_more_than_30_minutes_left
from config import AVAILABLE_HOURS
from database.session import SessionLocal
from datetime import datetime
from database.repository.reservation_repository import ReservationRepository

from database.models.banner import Banner
from database.models.user import User
from database.repository.user_repository import UserRepository

@bot.callback_query_handler(func=lambda c: c.data.startswith("select_day_"))
def show_free_hours_for_day(call: CallbackQuery):
    selected_date_str = call.data.replace("select_day_", "")
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()

    db = SessionLocal()
    try:
        reserveRepo = ReservationRepository(db)

        now = datetime.now()
        reserved_slots = reserveRepo.get_reservations_for_date(selected_date)
        reserved_times = {r.time for r in reserved_slots}

        markup = InlineKeyboardMarkup()
        any_available = False
        buttons = []

        for hour_str in AVAILABLE_HOURS:
            hour_time = datetime.strptime(hour_str, "%H:%M").time()

            # handle today time delay reservation rule 
            if selected_date == now.date():
                if not is_more_than_30_minutes_left(hour_str):
                    continue

            if hour_time in reserved_times:
                continue

            # تعیین یادداشت برای ساعت
            note = ""
            if hour_str in ["00:00", "00:30", "01:00", "01:30", "02:00"]:
                note = "(بامداد)"
            if hour_str == "02:00":
                note += " (⭐,پست آخر)"
            if "13:00" <= hour_str <= "17:00":
                note = "(-50%,تخفیف‌دار)"

            btn_text = f"{hour_str} {note}".strip()
            callback = f"reserve_{selected_date}_{hour_str}"
            buttons.append(InlineKeyboardButton(btn_text, callback_data=callback))
            any_available = True

        for i in range(0, len(buttons), 2):
            markup.row(*buttons[i:i+2])

        if not any_available:
            markup.add(InlineKeyboardButton("❌ هیچ ساعتی آزاد نیست", callback_data="none"))
        shamsi_date = convertToPersianDateStr(selected_date)
        weekday = get_weekday_persian(selected_date)
        bot.edit_message_text(
            text=f"⏰ ساعت‌های خالی برای <b>{shamsi_date}({weekday})</b> را انتخاب کنید:",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            reply_markup=markup,
            parse_mode="HTML"
        )
    finally:
        db.close()



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
        bot.answer_callback_query(call.id, "شما هیچ بنری ثبت نکرده‌اید.")
        return

    # Prepare buttons to show user their banners
    markup = InlineKeyboardMarkup(row_width=1)
    for b in user.banners :
        if b : 
            banner:Banner=b
            if not banner.is_deleted:
                markup.add(InlineKeyboardButton(banner.title, callback_data=f"banner_{banner.id}_{selected_date}_{selected_hour}"))

    bot.edit_message_text(text="📋 لطفاً بنری که می‌خواهید برای این زمان انتخاب کنید را انتخاب کنید.",
                          chat_id=call.message.chat.id,message_id= call.message.id , reply_markup=markup)
