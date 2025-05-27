from datetime import date, timedelta
from telebot.types import CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from app.telegram.handlers.other.exception_handler import catch_errors
from app.utils.markup.week_markup import show_reservation_day_selector
from app.utils.time_tools.covert_time_and_date import date_to_persian
from database.session import SessionLocal
from database.repository.reservation_repository import ReservationRepository
from database.repository.banner_repository import BannerRepository
from app.telegram.bot_instance import bot

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_reserve_all_dates"),is_admin=True)
@catch_errors(bot)
def show_all_reservation_days(call: CallbackQuery):
    chat_id=call.message.chat.id
    message_id=call.message.id
    today = date.today()
    start = today - timedelta(days=today.weekday())  # شروع هفته
    markup=show_reservation_day_selector( start)
    bot.edit_message_text(
        text="📅 انتخاب تاریخ برای نمایش رزروها:",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_reserve_all_dates_"),is_admin=True)
@catch_errors(bot)
def change_week_for_reservation(call: CallbackQuery):
    chat_id=call.message.chat.id
    message_id=call.message.id
    date_str = call.data.replace("admin_reserve_all_dates_", "")
    start = date.fromisoformat(date_str)
    markup=show_reservation_day_selector( start)
    bot.edit_message_text(
        text="📅 انتخاب تاریخ برای نمایش رزروها:",
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_reserve_day_"),is_admin=True)
@catch_errors(bot)
def show_reservations_for_day(call: CallbackQuery):
    db = SessionLocal()
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)

    day_str = call.data.replace("admin_reserve_day_", "")
    selected_day = date.fromisoformat(day_str)
    selected_day_shamsi=date_to_persian(selected_day)
    reservations = repo.get_reservations_for_date(selected_day)

    markup = InlineKeyboardMarkup(row_width=1)
    for reserve in reservations:
        banner = banner_repo.get_by_id(reserve.banner_id)
        banner_title = banner.title if banner else "بنر حذف شده"
        btn_text = f"{reserve.time.strftime('%H:%M')} | {reserve.user_id} | {banner_title} "
        markup.add(InlineKeyboardButton(btn_text, callback_data=f"admin_view_reserve_{reserve.id}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"📅 رزروهای تاریخ \n{selected_day_shamsi}:",
        reply_markup=markup
    )
