import re
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.telegram.states.user_state import ChargeStates, userState
from app.utils.notifiers.notify_admin import notify_admins_error
from config import ADMINS
from database.repository.bot_setting_repository import BotSettingRepository
from database.services.balance_services import charge_user_transaction
from database.session import SessionLocal


from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.message import get_message
from database.repository.user_repository import UserRepository

@bot.message_handler(content_types=["photo"], state=userState.waiting_for_pic)
@catch_errors(bot)
def handle_receipt(msg: Message):
    with bot.retrieve_data(user_id=msg.chat.id, chat_id=msg.chat.id) as data:
        amount = data["amount"]

    if not amount:
        bot.send_message(msg.chat.id, "❌ مبلغ مشخص نیست. لطفاً دوباره تلاش کنید.")
        return

    db = SessionLocal()
    try:
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
                "🔔 درخواست شارژ جدید از طرف کاربر:\n\n"
                f"{user_profile_text}\n\n"
                f"💳 مبلغ درخواستی: ✅{int(amount):,} تومان"
            )

            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("✅ تایید", callback_data=f"confirm_charge_{user.userid}_{amount}_{msg.message_id}_{msg.chat.id}"),
                InlineKeyboardButton("❌ رد", callback_data=f"reject_charge_{user.userid}_{msg.message_id}"),
                InlineKeyboardButton("✏️ تغییر مبلغ", callback_data=f"edit_charge_{user.userid}_{msg.message_id}")
            )

            bot.send_message(admin_id, caption, parse_mode="HTML", reply_to_message_id=pic_msg.message_id, reply_markup=markup)

        bot.send_message(msg.chat.id, "✅ رسید شما با موفقیت ارسال شد. منتظر تایید توسط ادمین باشید.")
        bot.delete_state(msg.from_user.id, msg.chat.id)
    finally:
        db.close()


