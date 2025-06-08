from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.telegram.states.user_state import ChargeStates

# Reject Charge Handler
@bot.callback_query_handler(func=lambda c: c.data.startswith("reject_charge_"), is_admin=True)
@catch_errors(bot)
def handle_reject_charge(call: CallbackQuery):
    key = call.data.replace("reject_charge_","")
    user_id, msg_id = key.split("_")

    markup_edited=InlineKeyboardMarkup()
    markup_edited.add(InlineKeyboardButton(text="❌این رسید رد شده است❌",callback_data="none"))
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup_edited)

    bot.send_message(call.message.chat.id, "📝 لطفاً دلیل رد درخواست را وارد کنید:")
    bot.set_state(state=ChargeStates.waiting_for_reject_reason, user_id=call.message.chat.id, chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data["target_user_id"] = int(user_id)
        data["msg_id"] = int(msg_id)


@bot.message_handler(state=ChargeStates.waiting_for_reject_reason, is_admin=True)
@catch_errors(bot)
def receive_reject_reason(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = int(data.get("target_user_id"))
        msg_id = int(data.get("msg_id"))

    bot.send_message(user_id, f"❌ درخواست شارژ شما توسط ادمین رد شد.\n📝 دلیل: {msg.text}" ,reply_to_message_id=int(msg_id))
    bot.send_message(msg.chat.id, "⛔️ پیام رد برای کاربر ارسال شد.")
    bot.delete_state(user_id=msg.chat.id, chat_id=msg.chat.id)
