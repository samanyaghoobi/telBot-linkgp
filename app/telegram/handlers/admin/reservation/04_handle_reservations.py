from datetime import datetime
from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.notifiers.notify_cancell_reservation import cancel_reservation_notifier
from app.utils.text_formatter.reservation_info import format_reservation_by_id, format_reservation_message
from app.utils.time_tools.novert_time_and_date import date_to_persian
from database.models.user import User
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from app.telegram.handlers.other.exception_handler import catch_errors
from database.base import SessionLocal
from database.services.reservation_service import cancel_reservation_transaction




# ▗▄▄▖ ▗▄▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▄▖ ▗▖  ▗▖▗▄▄▄▖    ▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖ ▗▄▖ 
# ▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌ ▐▌▐▌  ▐▌▐▌         █  ▐▛▚▖▐▌▐▌   ▐▌ ▐▌
# ▐▛▀▚▖▐▛▀▀▘ ▝▀▚▖▐▛▀▀▘▐▛▀▚▖▐▌  ▐▌▐▛▀▀▘      █  ▐▌ ▝▜▌▐▛▀▀▘▐▌ ▐▌
# ▐▌ ▐▌▐▙▄▄▖▗▄▄▞▘▐▙▄▄▖▐▌ ▐▌ ▝▚▞▘ ▐▙▄▄▖    ▗▄█▄▖▐▌  ▐▌▐▌   ▝▚▄▞▘
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
        bot.answer_callback_query(call.id, "❌ رزرو یافت نشد.")
        return

    user: User = user_repo.get_user(reservation.user_id)
    banner = banner_repo.get_by_id(reservation.banner_id)

    now = datetime.now()
    reserve_datetime = datetime.combine(reservation.date, reservation.time)
    can_cancel = (reserve_datetime - now).total_seconds() >= 5 * 60  # حداقل ۵ دقیقه تا رزرو


    msg= format_reservation_by_id(reservation_id=reservation.id)

    markup = InlineKeyboardMarkup(row_width=2)
    if can_cancel:
        markup.add(InlineKeyboardButton("❌ کنسل کردن رزرو", callback_data=f"admin_cancel_reserve_{reservation.id}"))
    if banner:
        markup.add(InlineKeyboardButton("🖼 نمایش بنر", callback_data=f"admin_getBanner_{reservation.id}"))
    markup.add(InlineKeyboardButton("🔙 بازگشت", callback_data=f"admin_reserve_day_{reservation.date.isoformat()}"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=msg,
        reply_markup=markup
    )



                                                                       
                                                                       


#  ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▄▖▗▖       ▗▄▄▖ ▗▄▄▄▖ ▗▄▄▖▗▄▄▖ ▗▄▄▄▖▗▖  ▗▖▗▄▄▄▖
# ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌   ▐▌       ▐▌ ▐▌▐▌   ▐▌   ▐▌ ▐▌▐▌   ▐▌  ▐▌▐▌   
# ▐▌   ▐▛▀▜▌▐▌ ▝▜▌▐▌   ▐▛▀▀▘▐▌       ▐▛▀▚▖▐▛▀▀▘ ▝▀▚▖▐▛▀▚▖▐▛▀▀▘▐▌  ▐▌▐▛▀▀▘
# ▝▚▄▄▖▐▌ ▐▌▐▌  ▐▌▝▚▄▄▖▐▙▄▄▖▐▙▄▄▖    ▐▌ ▐▌▐▙▄▄▖▗▄▄▞▘▐▌ ▐▌▐▙▄▄▖ ▝▚▞▘ ▐▙▄▄▖
                                                                       
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_cancel_reserve_"), is_admin=True)
@catch_errors(bot)
def admin_cancel_reservation(call: CallbackQuery):
    db = SessionLocal()
    res_repo = ReservationRepository(db)

    reserve_id = int(call.data.replace("admin_cancel_reserve_", ""))
    reservation = res_repo.get_by_id(reserve_id)

    result = cancel_reservation_transaction(db, reserve_id)
    if not result:
        bot.answer_callback_query(call.id, "❌ امکان لغو رزرو وجود ندارد.")
        return

    cancel_reservation_notifier(reservation,result,call.message.text)
    bot.delete_message(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id, "✅ رزرو با موفقیت لغو شد.")


    # نمایش مجدد اطلاعات رزرو پس از لغو
    call.data = f"admin_view_reserve_{reserve_id}"
    show_admin_reserve_detail(call)



                                                        
                                                        
                                                        


#  ▗▄▄▖▗▖ ▗▖ ▗▄▖ ▗▖ ▗▖    ▗▄▄▖  ▗▄▖ ▗▖  ▗▖▗▖  ▗▖▗▄▄▄▖▗▄▄▖ 
# ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌    ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌▐▛▚▖▐▌▐▌   ▐▌ ▐▌
#  ▝▀▚▖▐▛▀▜▌▐▌ ▐▌▐▌ ▐▌    ▐▛▀▚▖▐▛▀▜▌▐▌ ▝▜▌▐▌ ▝▜▌▐▛▀▀▘▐▛▀▚▖
# ▗▄▄▞▘▐▌ ▐▌▝▚▄▞▘▐▙█▟▌    ▐▙▄▞▘▐▌ ▐▌▐▌  ▐▌▐▌  ▐▌▐▙▄▄▖▐▌ ▐▌
@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_getBanner_"), is_admin=True)
@catch_errors(bot)
def show_banner_text(call: CallbackQuery):
    db = SessionLocal()
    res_repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)

    reserve_id = int(call.data.replace("admin_getBanner_", ""))
    reservation = res_repo.get_by_id(reserve_id)
    if not reservation:
        bot.answer_callback_query(call.id, "❌ رزرو یافت نشد.")
        return

    banner = banner_repo.get_by_id(reservation.banner_id)
    if not banner:
        bot.answer_callback_query(call.id, "❌ بنر یافت نشد.")
        return

    bot.send_message(chat_id=call.message.chat.id, text=banner.text)
    bot.answer_callback_query(call.id)
