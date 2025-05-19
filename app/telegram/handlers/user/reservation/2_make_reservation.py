from app.utils import notify_admin
from app.utils.markup.week_markup import show_week_for_navigation
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,Message
from app.telegram.bot_instance import bot
from app.utils.messages import get_message
from config import ADMINS
from database.base import SessionLocal
from datetime import datetime, timedelta
from app.telegram.handlers.exception_handler import catch_errors
from database.models.banner import Banner
from database.models.user import User
from database.repository.banner_repository import BannerRepository
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

############# show reserve information 
@bot.callback_query_handler(func=lambda c: c.data.startswith("banner_"))
def show_reservation_details(call: CallbackQuery):
    # Extract banner id, date, and time from callback data
    banner_id, selected_date, selected_hour = call.data.replace("banner_", "").split("_")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    selected_hour = selected_hour

    # Retrieve banner, user details, and price from the database
    db = SessionLocal()
    banner = db.query(Banner).filter(Banner.id == int(banner_id)).first()
    user = db.query(User).filter(User.userid == call.from_user.id).first()

    if not banner:
        bot.answer_callback_query(call.id, "بنر پیدا نشد.")
        return

    # Retrieve the price for the selected time
    setting_repo = BotSettingRepository(db)
    price = setting_repo.bot_setting_get("price_per_hour", "50")  # Default price if not found in DB #todo : makr it work

    # Prepare the confirmation message
    line = get_message("txt.line")
    message = f"✅ شما قصد دارید برای روز {selected_date} ساعت {selected_hour} بنر فوق را رزرو کنید:\n\n"
    message += f"🖼 بنر: {banner.title}\n"
    message_banner_text = f"{banner.text}\n"
    message += f"💰 قیمت: {price} تومان\n"
    message += f"💳 موجودی شما: {user.balance} تومان\n\n"
    message += "💰 برای تایید رزرو و کسر موجودی، تایید کنید."
    
    banner_msg=bot.edit_message_text(
        text=message_banner_text,
        chat_id=call.message.chat.id,
        message_id=call.message.id
    )
    # Prepare markup with confirmation and cancel buttons
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("✅ تایید رزرو", callback_data=f"confirm_reservation_{banner.id}_{selected_date}_{selected_hour}_{banner_msg.id}"),
        InlineKeyboardButton("❌ کنسل", callback_data=f"cancel_reservation_{banner_msg.id}")
    )
    

    bot.send_message(
        chat_id=call.message.chat.id,
        text=message,
        reply_to_message_id=banner_msg.id,
        reply_markup=markup
    )



#  ▗▄▄▖ ▗▄▖ ▗▖  ▗▖ ▗▄▄▖▗▄▄▄▖▗▖   
# ▐▌   ▐▌ ▐▌▐▛▚▖▐▌▐▌   ▐▌   ▐▌   
# ▐▌   ▐▛▀▜▌▐▌ ▝▜▌▐▌   ▐▛▀▀▘▐▌   
# ▝▚▄▄▖▐▌ ▐▌▐▌  ▐▌▝▚▄▄▖▐▙▄▄▖▐▙▄▄▖
# Handler to cancel the reservation and delete the message
@bot.callback_query_handler(func=lambda c: c.data.startswith("cancel_reservation_"))
def cancel_reservation(call: CallbackQuery):
    call.message.text
    banner_msg_id = call.data.replace("cancel_reservation_", "")

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
    # Extract the banner id, date, and time from the callback data
    banner_id, selected_date, selected_hour ,banner_msg_id= call.data.replace("confirm_reservation_", "").split("_")
    selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    selected_hour = selected_hour

    db = SessionLocal()
    userRepo = UserRepository(db)
    reserve_repo = ReservationRepository(db)
    setting_repo = BotSettingRepository(db)
    bannerRepo= BannerRepository(db)

    user = userRepo.get_user(call.from_user.id)
    banner = bannerRepo.get_by_id(banner_id=banner_id)
    banner_link=banner.link
    # Check if user has sufficient balance
    price = int(setting_repo.bot_setting_get("price_per_hour", "50"))  # Default price if not found in DB #todo : makr it work
    if user.balance < price and call.message.chat.id not in ADMINS:
        bot.send_message(call.message.chat.id, "❌ موجودی شما کافی نیست.")
        return
    # Start the transaction block
    try:
        # Decrease user's balance first
        userRepo.update_balance(user.userid, -price)
        
        # Create the reservation
        new_reservation = reserve_repo.create_reservation(
            user_id=user.userid,
            banner_id=int(banner_id),
            reserve_date=selected_date,
            reserve_time=selected_hour,
            link=banner_link,
            price=price
        )

        # Commit the transaction
        db.commit()
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=banner_msg_id)

        msg=bot.send_message(
            call.message.chat.id,
            f"✅ رزرو شما در تاریخ :  {selected_date} -  ساعت {selected_hour}  \n با موفقیت انجام شد. \n در ادامه بنر شما ارسال خواهد شد",
        )
        text=banner.text
        bot.reply_to(message=msg,text=text)

    except SQLAlchemyError as e:
        # If an error occurs, rollback the transaction and notify the user
        db.rollback()
        print("rollback---------------------------")
        notify_admin(bot, "db.rollback", e, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"❌ مشکلی در ثبت رزرو پیش آمد. لطفا دوباره تلاش کنید.")
        bot.error(e)
    except Exception as e:
        # db.rollback()
        notify_admin(bot, "db.rollback (Generic)", e, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"❌ خطایی رخ داد.")
