from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message
from app.utils.notifiers.notify_admin import notify_admins_error
from database.repository.user_repository import UserRepository
from database.services.balance_services import charge_user_transaction
from database.session import SessionLocal

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_charge_"))
@catch_errors(bot)
def confirm_charge(call: CallbackQuery):
    try:
        key = call.data.replace("confirm_charge_","")
        user_id, amount, msg_id,chat_id = key.split("_")
        user_id = int(user_id)
        amount = int(amount)


        db = SessionLocal()
        userRepo=UserRepository(db)
        old_balance = userRepo.get_user(user_id).balance
        success = charge_user_transaction(db, user_id=user_id, amount=amount)

        if success:
            user = userRepo.get_user(user_id)
            profile_text = get_message(
                "user.profile",
                user_id=user.userid,
                username=user.username,
                balance=user.balance,
                score=user.score
            )
            

            bot.send_message(
                chat_id,
                f"💰 <b>شارژ با موفقیت انجام شد!</b>\n\n"
                f"🔹 <b>موجودی قبلی:</b> <code>{old_balance:,}</code> هزار تومان\n"
                f"🔹 <b>میزان افزایش:</b> ✅<code>{(user.balance-old_balance):,}</code> هزار تومان\n"
                f"🔸 <b>موجودی جدید:</b> <code>{user.balance:,}</code> هزار تومان\n\n"
                f"{profile_text}",
                reply_to_message_id=int(msg_id),
                parse_mode="HTML"
              )
            
            markup_edited=InlineKeyboardMarkup()
            markup_edited.add(InlineKeyboardButton(text="✅این رسید تایید شده است✅",callback_data="none"))
            bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup_edited)

        else:
            bot.answer_callback_query(call.id, "❌ عملیات شارژ ناموفق بود.")
    except Exception as e:
        bot.answer_callback_query(call.id, "❌ خطا در پردازش تایید.")
        notify_admins_error(bot, "confirm_charge callback", e, user_info=call.from_user.id)
