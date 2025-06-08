from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.telegram.states.user_state import ChargeStates
from app.utils.message import get_message
from database.repository.user_repository import UserRepository
from database.services.balance_services import charge_user_transaction
from database.session import SessionLocal

# Edit Charge Handler
@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_charge_"), is_admin=True)
@catch_errors(bot)
def handle_edit_charge(call: CallbackQuery):
    key = call.data.replace("edit_charge_","")
    
    user_id, msg_id = key.split("_")

    markup_edited=InlineKeyboardMarkup()
    markup_edited.add(InlineKeyboardButton(text="⚠️✅این رسید تایید شده است(با تغییر مبلغ)✅⚠️",callback_data="none"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup_edited)
    
    bot.send_message(call.message.chat.id, "✏️ لطفاً مبلغ جدید را (به هزار تومان) وارد کنید:")
    bot.set_state(state=ChargeStates.waiting_for_edit_amount, user_id=call.message.chat.id, chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data["target_user_id"] = int(user_id)
        data["msg_id"] = int(msg_id)


@bot.message_handler(state=ChargeStates.waiting_for_edit_amount, is_admin=True)
@catch_errors(bot)
def receive_edited_amount(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, "❌ لطفاً فقط عدد وارد کنید.")
        return

    new_amount = int(msg.text)

    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = int(data.get("target_user_id"))
        msg_id = int(data.get("msg_id"))

    db = SessionLocal()
    userRepo=UserRepository(db)
    old_balance = userRepo.get_user(user_id).balance
    success = charge_user_transaction(db, user_id=user_id, amount=new_amount)

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
            msg.chat.id,
            f"💰 <b>شارژ با موفقیت انجام شد!</b>\n\n"
            f"🔹 <b>موجودی قبلی:</b> <code>{old_balance:,}</code> هزار تومان\n"
            f"🔹 <b>میزان افزایش:</b> ✅<code>{(user.balance-old_balance):,}</code> هزار تومان\n"
            f"🔸 <b>موجودی جدید:</b> <code>{user.balance:,}</code> هزار تومان\n\n"
            f"{profile_text}",
            reply_to_message_id=int(msg_id),
            parse_mode="HTML"
            )
        

    else:
        bot.send_message(msg.chat.id, "❌ خطا در انجام عملیات شارژ.")

    bot.delete_state(user_id=msg.chat.id, chat_id=msg.chat.id)
