from app.telegram.bot_instance import bot
from telebot.types import Message, CallbackQuery
from app.telegram.states.admin_state import AdminUserEditState
from app.utils.messages.user_profile import get_userProfile_and_markup
from database.session import SessionLocal
from database.repository.user_repository import UserRepository

# Callback for all user management actions
@bot.callback_query_handler(func=lambda c: any(c.data.startswith(prefix) for prefix in [
    "inc_balance_", "dec_balance_", "inc_score_", "dec_score_", "send_msg_"
]), is_admin=True)
def handle_user_management_callback(call: CallbackQuery):
    data_parts = call.data.split("_")
    action, user_id = data_parts[0] + "_" + data_parts[1], int(data_parts[2])


    if action.startswith("send_msg"):
        bot.send_message(call.message.chat.id, "📝 لطفاً پیام موردنظر برای کاربر را وارد کنید:")
        bot.set_state(user_id= call.message.chat.id,chat_id=  call.message.chat.id,state= AdminUserEditState.waiting_for_message)
    else:
        bot.send_message(call.message.chat.id, "🔢 لطفاً مقدار موردنظر (عدد صحیح) را وارد کنید:")
        bot.set_state(user_id= call.message.chat.id, chat_id= call.message.chat.id,state= AdminUserEditState.waiting_for_amount)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data["edit_target_user_id"] = user_id
        data["edit_action"] = action
        data["reply_to"] = call.message.message_id
        data["call.msg.id"]=call.message.id
        data["replied"]=call.message.reply_to_message


#send message
@bot.message_handler(state=AdminUserEditState.waiting_for_message, is_admin=True)
def receive_admin_message_for_user(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = data["edit_target_user_id"]
        reply_to = data.get("reply_to")

    bot.send_message(user_id, f"📩 پیام از ادمین:\n{msg.text}")
    bot.send_message(msg.chat.id, "✅ پیام ارسال شد.", reply_to_message_id=reply_to)
    bot.delete_state(msg.from_user.id, msg.chat.id)



@bot.message_handler(state=AdminUserEditState.waiting_for_amount, is_admin=True)
def receive_admin_amount_input(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, "❌ لطفاً فقط عدد وارد کنید.")
        return

    amount = int(msg.text)

    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        user_id = data["edit_target_user_id"]
        action = data["edit_action"]
        reply_to = data.get("reply_to")
        replied = data.get("replied")
        msg_id=data["call.msg.id"]

    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_user(user_id)
    if not user:
        bot.send_message(msg.chat.id, "❌ کاربر یافت نشد.")
        return

    before_balance = user.balance
    before_score = user.score

    if action == "inc_balance":
        repo.update_balance(user_id, amount)
    elif action == "dec_balance":
        result=repo.update_balance(user_id, -amount)
    elif action == "inc_score":
        repo.update_score(user_id, amount)
    elif action == "dec_score":
        repo.update_score(user_id, -amount)

    updated_user = repo.get_user(user_id)
    db.close()
    text = ""
    if action.endswith("balance"):
        text = (
            f"💰 <b>تغییر موجودی انجام شد!</b>\n\n"
            f"🔹 <b>موجودی قبلی:</b> <code>{before_balance:,}</code> هزار تومان\n"
            f"🔹 <b>تغییر:</b> {'✅' if 'inc' in action else '❌'}<code>{amount:,}</code> هزار تومان\n"
            f"🔸 <b>موجودی جدید:</b> <code>{updated_user.balance:,}</code> هزار تومان"
        )
    else:
        text = (
            f"🎯 <b>تغییر امتیاز انجام شد!</b>\n\n"
            f"🔹 <b>امتیاز قبلی:</b> <code>{before_score:,}</code>\n"
            f"🔹 <b>تغییر:</b> {'✅' if 'inc' in action else '❌'}<code>{amount:,}</code>\n"
            f"🔸 <b>امتیاز جدید:</b> <code>{updated_user.score:,}</code>"
        )
    bot.delete_message(chat_id=msg.chat.id,message_id=msg_id)

    user_profile,markup=get_userProfile_and_markup(user)
    message_info=bot.send_message(msg.chat.id, user_profile, parse_mode="HTML",reply_markup=markup)

    bot.send_message(msg.chat.id, text, parse_mode="HTML", reply_to_message_id=message_info.id)
    bot.delete_state(msg.from_user.id, msg.chat.id)

    # ✅ Notify user
    notify_text = ""
    if action.endswith("balance"):
        notify_text = (
            f"💼 موجودی شما توسط ادمین تغییر کرد.\n"
            f"{'➕' if 'inc' in action else '➖'} مبلغ: <b>{amount:,}</b> هزار تومان\n"
            f"🔹 موجودی جدید شما: <b>{user.balance:,}</b> هزار تومان"
        )
    else:
        notify_text = (
            f"🏅 امتیاز شما توسط ادمین تغییر کرد.\n"
            f"{'➕' if 'inc' in action else '➖'} امتیاز: <b>{amount:,}</b>\n"
            f"🔹 امتیاز جدید شما: <b>{user.score:,}</b>"
        )

    bot.send_message(user.userid, notify_text, parse_mode="HTML")

