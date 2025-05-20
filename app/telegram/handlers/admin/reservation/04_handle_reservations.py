from datetime import datetime
from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup

from app.utils.time_tools.novert_time_and_date import to_persian_date_str
from database.models.user import User
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from app.telegram.handlers.other.exception_handler import catch_errors

from database.base import SessionLocal
from database.services.reservation_service import cancel_reservation_transaction

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_view_reserve_"), is_admin=True)
@catch_errors(bot)
def show_admin_reserve_detail(call: CallbackQuery):
    db = SessionLocal()
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)
    user_repo = UserRepository(db)

    reserve_id = int(call.data.replace("admin_view_reserve_", ""))
    reservation = repo.get_by_id(reserve_id)

    if not reservation:
        bot.answer_callback_query(call.id, "رزرو یافت نشد.")
        return

    user: User = user_repo.get_user(reservation.user_id)
    banner = banner_repo.get_by_id(reservation.banner_id)

    now = datetime.now()
    reserve_datetime = datetime.combine(reservation.date, reservation.time)
    can_cancel = (reserve_datetime - now).total_seconds() >= 5 * 60  # حداقل ۵ دقیقه

    # اطلاعات
    msg = (
        f"📅 تاریخ رزرو: {to_persian_date_str(reservation.date)}\n"
        f"⏰ ساعت: {reservation.time.strftime('%H:%M')}\n"
        f"🧑‍💼 کاربر:  ({user.userid})\n"
        f"💳 موجودی: {user.balance:,} تومان\n"
        f"🏷 بنر: {banner.title if banner else 'بنر حذف شده'}\n"
        f"🔗 لینک: {reservation.link}\n"
        f"💰 مبلغ رزرو: {reservation.price:,} تومان\n"
    )

    # مارکاپ
    markup = InlineKeyboardMarkup(row_width=2)
    if can_cancel:
        markup.add(InlineKeyboardButton("❌ کنسل کردن رزرو", callback_data=f"admin_cancel_reserve_{reservation.id}"))
    markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data=f"admin_reserve_day_{reservation.date.isoformat()}"))

    # ارسال متن و بنر
    if banner:
        bot.send_message(call.message.chat.id, banner.text)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=msg,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_cancel_reserve_"), is_admin=True)
@catch_errors(bot)
def admin_cancel_reservation(call: CallbackQuery):
    db = SessionLocal()
    reserve_id = int(call.data.replace("admin_cancel_reserve_", ""))

    success = cancel_reservation_transaction(db, reserve_id=reserve_id)

    if not success:
        bot.answer_callback_query(call.id, "❌ امکان لغو رزرو وجود ندارد.")
        return

    # نمایش مجدد جزئیات رزرو
    bot.answer_callback_query(call.id, "✅ رزرو با موفقیت لغو شد.")
    call.data = f"admin_view_reserve_{reserve_id}"
    show_admin_reserve_detail(call)
