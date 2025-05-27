from datetime import date, datetime, timedelta
import jdatetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from database.session import SessionLocal
from database.models.banner import Banner
from database.models.reservation import Reservation
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository

@bot.callback_query_handler(func=lambda c: c.data.startswith("show_reservation_"))
def show_single_reservation(call: CallbackQuery):
    db = SessionLocal()
    reservation_id ,call_data= call.data.replace("show_reservation_", "").split(":")
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)

    reservation = repo.get_by_id(reservation_id)
    if not reservation:
        bot.answer_callback_query(call.id, "رزرو یافت نشد.", show_alert=True)
        return

    banner = banner_repo.get_by_id(reservation.banner_id)
    banner_text = banner.text if banner else "بنر نامشخص"
    banner_title = banner.title if banner else "بنر نامشخص"

    # Show banner by editing current message
    banner_msg=bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=banner_text
    )

    # Format date
    day_shamsi = jdatetime.date.fromgregorian(date=reservation.date)
    jdate_str = f"{day_shamsi.month}/{day_shamsi.day}"

    # Send details as reply
    info = (
        f"📄 اطلاعات رزرو:\n"
        f"🖼 عنوان بنر: {banner_title}\n"
        f"📅 تاریخ: {jdate_str}\n"
        f"⏰ ساعت: {reservation.time.strftime('%H:%M')}\n"
        f"💰 قیمت: {reservation.price} تومان"
    )

    # Action buttons
    markup = InlineKeyboardMarkup(row_width=2)

    now = datetime.now()
    can_cancel = (
        reservation.date > now.date() or
        (reservation.date == now.date() and
         datetime.combine(reservation.date, reservation.time) - now >= timedelta(minutes=30))
    )


    if can_cancel:
        markup.add(
            InlineKeyboardButton("🔄 تعویض بنر", callback_data=f"change_banner_{reservation.id}")
        )
        markup.add(
            InlineKeyboardButton("❌ کنسل کردن رزرو", callback_data=f"cancel_reservation_{reservation.id}")
        )
    else:
        markup.add(
            InlineKeyboardButton("⏳ خیلی دیره برای کنسل یا تغییر", callback_data="none")
        )
    markup.add(
        InlineKeyboardButton(text="برگشت به منوی قبل",callback_data=f"${call_data}_${banner_msg.id}")
    )
    msg = bot.send_message(
        chat_id=call.message.chat.id,
        text=info,
        reply_to_message_id=call.message.id,
        reply_markup=markup
    )


    