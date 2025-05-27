from database.models.reservation import Reservation


from telebot.types import Message
from database.models.reservation import Reservation
from app.telegram.bot_instance import bot
from app.utils.time_tools.covert_time_and_date import date_to_persian


def cancel_reservation_notifier(reservation: Reservation, result: bool,reserve_info:str=None, reason: str = None):
    user_id = reservation.user_id

    if not result:
        return  # در صورت شکست تراکنش، پیام ارسال نشود

    # دلیل لغو
    reason = reason or "❌ رزرو شما توسط ادمین لغو شده است."
    if reserve_info:
        message=f"{reason} \n {reserve_info} \n🔁 موجودی شما افزایش یافت."
    else:
        # تبدیل تاریخ به شمسی
        shamsi_date = date_to_persian(reservation.date)
        time_str = reservation.time.strftime("%H:%M")

        # پیام نهایی
        message = (
            f"{reason}\n\n"
            f"📅 تاریخ: {shamsi_date}\n"
            f"⏰ ساعت: {time_str}\n"
            f"💰 مبلغ بازگشتی: {reservation.price:,} تومان\n"
            f"🔁 موجودی شما افزایش یافت."
        )
    # message = format_reservation_by_id(reservation_id=reservation.)
    try:
        bot.send_message(chat_id=user_id, text=message)
    except Exception as e:
        print(f"❌ Failed to notify user {user_id}: {e}")
