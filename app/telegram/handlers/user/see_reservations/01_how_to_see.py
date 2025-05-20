from datetime import date, datetime, timedelta
import jdatetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.messages import get_message
from database.base import SessionLocal
from database.models.banner import Banner
from database.models.reservation import Reservation
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository

@bot.message_handler(func=lambda m: m.text == get_message("btn.my_reservations"))
def my_reservation(message: Message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🕓 فقط رزروهای آینده", callback_data="show_future_reservations"),
        InlineKeyboardButton("🔁 نمایش همه رزروها", callback_data="show_all_reservations")
    )
    bot.send_message(
        message.chat.id,
        "📋 لطفاً انتخاب کن کدوم نوع رزروها رو می‌خوای ببینی:",
        reply_markup=markup
    )
    
    #todo : handle  back btn remove banner
@bot.callback_query_handler(func=lambda c: c.data in ["show_future_reservations", "show_all_reservations"])
def show_reservations(call: CallbackQuery):
    db = SessionLocal()
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)
    user_id = call.from_user.id
    today = date.today()
    now = datetime.now()
    call_data= call.data
    if call_data == "show_future_reservations":
        reservations = repo.get_upcoming_by_user(user_id)
        title = "🕓 رزروهای آینده شما:"
    else:
        reservations = repo.get_all_by_user(user_id)
        title = "📋 تمام رزروهای شما:"

    if not reservations:
        bot.answer_callback_query(call.id, text="هیچ رزروی پیدا نشد.", show_alert=True)
        return

    markup = InlineKeyboardMarkup(row_width=1)
    for reserve in reservations:
        is_future = (
            reserve.date > today or
            (reserve.date == today and reserve.time > now.time()) or
            (call.data == "show_future_reservations")
        )
        # Convert to Jalali
        day_shamsi = jdatetime.date.fromgregorian(date=reserve.date)
        show_year = day_shamsi.year != jdatetime.date.today().year
        jdate_str = f"{day_shamsi.month}/{day_shamsi.day}"
        if show_year:
            jdate_str = f"{day_shamsi.year}/{jdate_str}"

        # Get banner title
        banner = banner_repo.get_by_id(reserve.banner_id)
        banner_title = banner.title if banner else "بنر نامشخص"

        icon = "🟢" if is_future  else "⚪️"
        button_text = f"{icon} {banner_title} | {jdate_str} - {reserve.time.strftime('%H:%M')}"
        markup.add(InlineKeyboardButton(button_text, callback_data=f"show_reservation_{reserve.id}:{call_data}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=title,
        reply_markup=markup
    )


