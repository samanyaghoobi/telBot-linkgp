from datetime import date, timedelta
from telebot.types import CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from app.telegram.handlers.other.exception_handler import catch_errors
from database.session import SessionLocal
from database.repository.reservation_repository import ReservationRepository
from database.repository.banner_repository import BannerRepository
from app.telegram.bot_instance import bot

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_reserve_upcoming"),is_admin=True)
@catch_errors(bot)
def show_today_reservations(call: CallbackQuery):
    db = SessionLocal()
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)

    today = date.today()
    reservations = repo.get_reservations_from_date(today)

    markup = InlineKeyboardMarkup(row_width=1)
    for reserve in reservations:
        banner = banner_repo.get_by_id(reserve.banner_id)
        banner_title = banner.title if banner else "بنر حذف شده"
        btn_text = f"{reserve.date} | {reserve.time.strftime('%H:%M')} | {reserve.user_id} | {banner_title} "
        markup.add(InlineKeyboardButton(btn_text,  callback_data=f"admin_view_reserve_{reserve.id}"))

    markup.add(InlineKeyboardButton("➡️ رفتن به فردا", callback_data=f"admin_reserve_day_{(today + timedelta(days=1)).isoformat()}"))
    bot.edit_message_text(
        text="رزروهای امروز به بعد:",
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
