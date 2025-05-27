from datetime import date, timedelta
from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery,Message,InlineKeyboardButton,InlineKeyboardMarkup
from app.telegram.exception_handler import catch_errors
from database.session import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from database.services.reservation_service import reserve_custom_range_transaction

AVAILABLE_HOURS = [
    "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "18:30",
    "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
    "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00", "01:30", "02:00"
]

# handler for starting custom range reservation
@bot.callback_query_handler(func=lambda c: c.data == "customReservation")
@catch_errors(bot)
def ask_custom_range_length(call: CallbackQuery):
    bot.set_state(call.from_user.id, "waiting_range_days", call.message.chat.id)
    bot.send_message(call.message.chat.id, "📌 چند روز متوالی می‌خواهی رزرو کنی؟ (بین ۳ تا ۳۰ عدد وارد کن)")


# state handler to receive number of days
@bot.message_handler(state="waiting_range_days")
@catch_errors(bot)
def handle_custom_range_days(msg: Message):
    db = SessionLocal()
    try:
        days = int(msg.text.strip())
    except ValueError:
        bot.send_message(msg.chat.id, "❌ لطفاً فقط یک عدد بین ۳ تا ۳۰ وارد کن.")
        return

    if days < 3 or days > 30:
        bot.send_message(msg.chat.id, "❌ عدد وارد شده باید بین ۳ تا ۳۰ باشد.")
        return

    from_date = date.today()
    to_date = from_date + timedelta(days=days - 1)

    repo = ReservationRepository(db)
    setting_repo = BotSettingRepository(db)
    # all_hours = get_available_hours_from_setting(setting_repo) #todo
    all_hours=AVAILABLE_HOURS
    free_hours = repo.get_fully_free_hours(from_date, to_date, all_hours)

    if not free_hours:
        bot.send_message(msg.chat.id, "❌ در این بازه هیچ ساعتی به‌طور کامل آزاد نیست.")
        return

    markup = InlineKeyboardMarkup(row_width=3)
    rows = [free_hours[i:i+3] for i in range(0, len(free_hours), 3)]
    for row in rows:
        buttons = [
            InlineKeyboardButton(f"{h}", callback_data=f"select_hour_range_{days}_{h}")
            for h in row
        ]
        markup.row(*buttons)

    bot.send_message(msg.chat.id, "⏰ یکی از ساعت‌هایی که در کل این بازه آزاد است را انتخاب کن:", reply_markup=markup)
    bot.delete_state(msg.from_user.id, msg.chat.id)


# handler to select hour and show banners
@bot.callback_query_handler(func=lambda c: c.data.startswith("select_hour_range_"))
@catch_errors(bot)
def choose_banner_for_range(call: CallbackQuery):
    parts = call.data.replace("select_hour_range_", "").split("_")
    days = int(parts[0])
    hour_str = parts[1]

    db = SessionLocal()
    user_repo = UserRepository(db)
    user = user_repo.get_user(call.from_user.id)

    if not user or not user.banners:
        bot.send_message(call.message.chat.id, "❌ شما هیچ بنری ثبت نکرده‌اید.")
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for banner in user.banners:  # type: Banner
        if banner.is_deleted:
            continue
        markup.add(InlineKeyboardButton(banner.title, callback_data=f"confirm_range_reserve_{days}_{hour_str}_{banner.id}"))

    bot.send_message(call.message.chat.id, "🖼 لطفاً بنری که می‌خواهی رزرو شود را انتخاب کن:", reply_markup=markup)


# confirm reservation and call transaction
@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_range_reserve_"))
@catch_errors(bot)
def confirm_custom_range_reserve(call: CallbackQuery):
    db = SessionLocal()
    parts = call.data.replace("confirm_range_reserve_", "").split("_")
    days = int(parts[0])
    hour = parts[1]
    banner_id = int(parts[2])

    user_id = call.from_user.id
    from_date = date.today()
    to_date = from_date + timedelta(days=days - 1)

    result, message = reserve_custom_range_transaction(db, user_id, banner_id, from_date, to_date, hour)
    bot.send_message(call.message.chat.id, message)


# service/reservation_service.py

# repository/reservation_repository.py


# # ابزار گرفتن ساعات قابل رزرو از تنظیمات
# def get_available_hours_from_setting(setting_repo):
#     from app.config.constants import DEFAULT_AVAILABLE_HOURS
#     raw = setting_repo.bot_setting_get("AVAILABLE_HOURS", None)
#     if not raw:
#         return DEFAULT_AVAILABLE_HOURS
#     return [x.strip() for x in raw.split(",") if x.strip()]
