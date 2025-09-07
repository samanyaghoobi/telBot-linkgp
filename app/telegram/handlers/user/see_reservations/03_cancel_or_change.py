from datetime import  datetime, timedelta
from telebot.types import   CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.markup.banner_list import build_user_banner_list_markup
from app.utils.message import get_message
from database.session import SessionLocal
from database.models.reservation import Reservation
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from database.services.reservation_service import cancel_reservation_transaction

@bot.callback_query_handler(func=lambda c: c.data.startswith("cancel_reservation_"))
@catch_errors(bot)
def cancel_reservation_action(call: CallbackQuery):
    reservation_id = int(call.data.replace("cancel_reservation_", ""))
    db = SessionLocal()
    try:
        repo = ReservationRepository(db)
        reservation = db.query(Reservation).get(reservation_id)

        if not reservation:
            bot.answer_callback_query(call.id, "رزرو یافت نشد.", show_alert=True)
            return

        now = datetime.now()
        res_datetime = datetime.combine(reservation.date, reservation.time)
        # Enforce user cancellation window (must be >= 30 minutes left)
        if res_datetime - now < timedelta(minutes=30):
            bot.answer_callback_query(call.id, "❌ امکان کنسل کردن نیست. کمتر از ۳۰ دقیقه تا زمان رزرو باقی‌ست.", show_alert=True)
            return

        # Cancel reservation with refund transactionally
        success = cancel_reservation_transaction(db, reservation_id)
        if not success:
            bot.answer_callback_query(call.id, "❌ خطا در لغو رزرو. کمی بعد دوباره تلاش کنید.", show_alert=True)
            return

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="❌ رزرو با موفقیت لغو شد و مبلغ به حساب شما برگشت."
        )
    finally:
        db.close()

    
@bot.callback_query_handler(func=lambda c: c.data.startswith("change_banner_"))
@catch_errors(bot)
def choose_new_banner(call: CallbackQuery):
    reservation_id = int(call.data.replace("change_banner_", ""))
    db = SessionLocal()
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user(call.from_user.id)

        if not user or not user.banners:
            bot.answer_callback_query(call.id, "شما هیچ بنری ثبت نکرده‌اید.")
            return

        # دکمه‌ها بساز با شناسه رزرو به عنوان پیوست
        markup = build_user_banner_list_markup(user_id=user.userid, callback_data=f"apply_banner_{reservation_id}_")
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📋 لطفاً یک بنر برای جایگزینی انتخاب کنید:",
            reply_markup=markup
        )
    finally:
        db.close()

@bot.callback_query_handler(func=lambda c: c.data.startswith("apply_banner_"))
@catch_errors(bot)
def apply_new_banner(call: CallbackQuery):
    parts = call.data.replace("apply_banner_", "").split("_")
    reservation_id = int(parts[0])
    new_banner_id = int(parts[1])

    db = SessionLocal()
    try:
        bannerRepo = BannerRepository(db)
        reserveRepo = ReservationRepository(db)
        reservation = reserveRepo.get_by_id(reservation_id)
        banner = bannerRepo.get_by_id(new_banner_id)
        if not reservation or not banner:
            bot.answer_callback_query(call.id, "بنر یا رزرو معتبر نیست.")
            return

        # Update banner
        reservation.banner_id = banner.id
        reservation.link = banner.link
        db.commit()

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="✅ بنر با موفقیت تغییر یافت."
        )
    finally:
        db.close()
