import re
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
from app.telegram.states.user_state import userState
from app.utils.notifiers.notify_admin import notify_admins_error
from config import ADMINS
from database.repository.bot_setting_repository import BotSettingRepository
from database.services.balance_services import charge_user_transaction
from database.session import SessionLocal


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.messages import get_message
from database.repository.user_repository import UserRepository

@bot.message_handler(content_types=["photo"], state=userState.waiting_for_pic)
@catch_errors(bot)
def handle_receipt(msg: Message):
    with bot.retrieve_data(user_id=msg.chat.id, chat_id=msg.chat.id) as data:
        amount = data.get("amount")

    if not amount:
        bot.send_message(msg.chat.id, "❌ مبلغ مشخص نیست. لطفاً دوباره تلاش کنید.")
        return

    db = SessionLocal()
    user_repo = UserRepository(db)
    user = user_repo.get_user(msg.from_user.id)

    if not user:
        bot.send_message(msg.chat.id, "❌ کاربر یافت نشد.")
        return

    # Build user profile text
    user_profile_text = get_message(
        "user.profile",
        user_id=user.userid,
        username=user.username or "ناشناس",
        balance=user.balance,
        score=user.score,
    )

    for admin_id in ADMINS:
        pic_msg = bot.forward_message(admin_id, msg.chat.id, msg.message_id)

        caption = (
            f"🔔 درخواست شارژ جدید از طرف کاربر:\n\n"
            f"{user_profile_text}\n\n"
            f"💳 مبلغ درخواستی: {amount:,} تومان"
        )

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("✅ تایید", callback_data=f"confirm_charge_{user.userid}_{amount}_{pic_msg.message_id}_{user.balance}"),
            InlineKeyboardButton("❌ رد", callback_data=f"reject_charge_{user.userid}_{pic_msg.message_id}"),
            InlineKeyboardButton("✏️ تغییر مبلغ", callback_data=f"edit_charge_{user.userid}_{pic_msg.message_id}")
        )

        bot.send_message(admin_id, caption, parse_mode="HTML", reply_to_message_id=pic_msg.message_id, reply_markup=markup)

    bot.send_message(msg.chat.id, "✅ رسید شما با موفقیت ارسال شد. منتظر تایید توسط ادمین باشید.")
    bot.delete_state(msg.from_user.id, msg.chat.id)

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_charge_"))
@catch_errors(bot)
def confirm_charge(call: CallbackQuery):
    try:
        key = call.data.replace("confirm_charge_","")
        user_id, amount, msg_id, old_balance = key.split("_")
        user_id = int(user_id)
        amount = int(amount)
        old_balance = int(old_balance)

        db = SessionLocal()
        success = charge_user_transaction(db, user_id=user_id, amount=amount)

        if success:
            new_balance = old_balance + amount
            bot.answer_callback_query(call.id, "✅ شارژ تایید شد.")

            bot.send_message(
                user_id,
                f"✅ شارژ {amount:,} تومان با موفقیت انجام شد.\n"
                f"💰 موجودی قبلی: {old_balance:,} هزار تومان\n"
                f"💰 موجودی جدید: {new_balance:,} هزار تومان"
            )

            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            bot.send_message(
                call.message.chat.id,
                f"🎉 موجودی از {old_balance:,} ➡️ {new_balance:,} هزار تومان افزایش یافت.",
                reply_to_message_id=int(msg_id)
            )
        else:
            bot.answer_callback_query(call.id, "❌ عملیات شارژ ناموفق بود.")
    except Exception as e:
        bot.answer_callback_query(call.id, "❌ خطا در پردازش تایید.")
        notify_admins_error(bot, "confirm_charge callback", e, user_info=call.from_user.id)
