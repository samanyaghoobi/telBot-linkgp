from app.utils.notifiers import notify_admin
from app.utils.markup.week_markup import show_week_for_navigation
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,Message
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from app.utils.priceing import get_price_from_db_for_time
from app.utils.text_formatter.reservation_info import format_reservation_by_id
from app.utils.time_tools.covert_time_and_date import convertToPersianDateStr
from app.utils.time_tools.other import get_weekday_persian, is_more_than_30_minutes_left
from config import ADMINS
from database.session import SessionLocal
from datetime import datetime, timedelta
from app.telegram.exception_handler import catch_errors
from database.models.banner import Banner
from database.models.user import User
from database.repository.banner_repository import BannerRepository
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

from database.services.reservation_service import reserve_banner_transaction

############# show reserve information 
@bot.callback_query_handler(func=lambda c: c.data.startswith("banner_"))
def show_reservation_details(call: CallbackQuery):
    # Extract banner id, date, and time from callback data
    banner_id, selected_date, selected_hour = call.data.replace("banner_", "").split("_")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    # Retrieve banner, user details, and price from the database
    db = SessionLocal()
    try:
        banner = db.query(Banner).filter(Banner.id == int(banner_id)).first()
        user = db.query(User).filter(User.userid == call.from_user.id).first()

        if not banner:
            bot.answer_callback_query(call.id, "بنر پیدا نشد.")
            return

        # Retrieve the price for the selected time
        #todo : makr it work
        price = get_price_from_db_for_time(selected_hour) # Default price if not found in DB 
        shamsi_date=convertToPersianDateStr(selected_date)
        weekday=get_weekday_persian(selected_date)
        # Prepare the confirmation message
        message =get_message("user.msg.reserve.confirm",    selected_date=shamsi_date,weekday=weekday,
        selected_hour=selected_hour,
        banner_title=banner.title,
        banner_text=banner.text,
        price=price,
        balance=user.balance)
        message_banner_text = f"{banner.text}\n"
        banner_msg=bot.edit_message_text(
            text=message_banner_text,
            chat_id=call.message.chat.id,
            message_id=call.message.id
        )
        # Prepare markup with confirmation and cancel buttons
        markup = InlineKeyboardMarkup(row_width=2)
        if  int(user.balance) <  int(price):
            markup.add(InlineKeyboardButton(get_message("user.balanceIncrease"),callback_data=get_message("user.balanceIncrease")))
            bot.send_message(reply_to_message_id=call.message.id,chat_id=call.message.chat.id,text=message+"\n\n"+get_message("error.user.notEnoughBalance"),reply_markup=markup)
            return
        markup.add(
            InlineKeyboardButton("✅ تایید رزرو", callback_data=f"confirm_reservation_{banner.id}_{selected_date}_{selected_hour}_{banner_msg.id}"),
            InlineKeyboardButton("❌ بیخیال", callback_data=f"forget_reservation_{banner_msg.id}")
        )
        

        bot.send_message(
            chat_id=call.message.chat.id,
            text=message,
            reply_to_message_id=banner_msg.id,
            reply_markup=markup
        )
    finally:
        db.close()



#  ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▄▖▗▖   
# ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌   ▐▌   
# ▐▌   ▐▛▀▜▌▐▌ ▝▜▌▐▌   ▐▛▀▀▘▐▌   
# ▝▚▄▄▖▐▌ ▐▌▐▌  ▐▌▝▚▄▄▖▐▙▄▄▖▐▙▄▄▖
# Handler to cancel the reservation and delete the message
@bot.callback_query_handler(func=lambda c: c.data.startswith("forget_reservation_"))
def cancel_reservation(call: CallbackQuery):
    
    banner_msg_id = call.data.replace("forget_reservation_", "")

    # Simply delete the message if the user cancels
    bot.delete_message(chat_id=call.message.chat.id, message_id=banner_msg_id)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    bot.send_message(chat_id=call.message.chat.id, text="رزرو کنسل شد.")

#  ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▄▄▄▖▗▄▄▖ ▗▖  ▗▖
# ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌     █  ▐▌ ▐▌▐▛▚▞▜▌
# ▐▌   ▐▌ ▐▌▐▌ ▝▜▌▐▛▀▀▘  █  ▐▛▀▚▖▐▌  ▐▌
# ▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▐▌   ▗▄█▄▖▐▌ ▐▌▐▌  ▐▌
                                     
                                     

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_reservation_"))
@catch_errors(bot)
def confirm_reservation(call: CallbackQuery):
    # Extract parameters from callback data
    banner_id, selected_date, selected_hour, banner_msg_id = call.data.replace("confirm_reservation_", "").split("_")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    db = SessionLocal()
    try:
        userRepo = UserRepository(db)
        bannerRepo = BannerRepository(db)
        reservationRepo = ReservationRepository(db)

        user = userRepo.get_user(call.from_user.id)
        banner = bannerRepo.get_by_id(banner_id=banner_id)
        #todo fix pricing
        # price = int(setting_repo.bot_setting_get("price_per_hour", "50"))
        price = get_price_from_db_for_time(selected_hour)
        #banner existence
        if not user or not banner:
            bot.send_message(call.message.chat.id, "❌ اطلاعات کاربر یا بنر یافت نشد.")
            return

        # link duplication
        duplicated_link=reservationRepo.is_duplicate_link_for_date(target_date=selected_date,link=banner.link )
        if duplicated_link:
            bot.delete_message(call.message.chat.id,call.message.id)
            bot.send_message(
            chat_id=call.message.chat.id,
            text=(
                "⚠️ <b>امکان ثبت این رزرو وجود ندارد.</b>\n\n"
                "برای هر روز تنها یک بار می‌توان از هر لینک استفاده کرد.\n"
                "لینکی که وارد کرده‌اید قبلاً برای این تاریخ ثبت شده است. ❌"
            ),
            parse_mode="HTML")

            return
        # handle today time delay reservation rule 
        now = datetime.now()
        if selected_date == now.date():
            if not is_more_than_30_minutes_left(selected_hour):
                bot.delete_message(call.message.chat.id,call.message.id)
                bot.send_message(call.message.chat.id,text="امکان رزرو این ساعت وجود ندارد❌")
        # Call transactional reservation service
        reservation = reserve_banner_transaction(
            db=db,
            user_id=user.userid,
            banner_id=banner.id,
            reserve_date=selected_date,
            reserve_time=selected_hour,
            price=price,
            link=banner.link
        )
        if not reservation:
            bot.send_message(call.message.chat.id, "❌ رزرو انجام نشد. لطفاً دوباره تلاش کنید.")
            return

        # If successful, delete previous messages and send confirmation
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=banner_msg_id)

        message = format_reservation_by_id(reservation_id=reservation.id)
        bot.send_message(
            call.message.chat.id,
            f"اطلاعات رزرو شما:\n{message}\n\n✅ رزرو شما با موفقیت ثبت شد."
        )
    finally:
        db.close()
