from app.utils.message import get_message
from app.utils.paging_inline_btn import create_pagination_for_users
from telebot.types import InlineKeyboardMarkup
from app.telegram.bot_instance import bot
from database.session import SessionLocal
from database.repository.user_repository import UserRepository 
from telebot.types import CallbackQuery,InlineKeyboardButton,Message

@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.user_list"), is_admin=True)
def user_list(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    db = SessionLocal()
    repo = UserRepository(db)
    users = repo.get_all_users()

    markup = create_pagination_for_users(users, 0)
    bot.send_message(
        chat_id=msg.chat.id,
        text=get_message("msg.admin.user_list"),
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_") or call.data.startswith("next_"))
def paginate_user_list(call: CallbackQuery):
    db = SessionLocal()
    repo = UserRepository(db)
    users = repo.get_all_users()

    page = int(call.data.split("_")[1])
    markup = create_pagination_for_users(users, page)

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("users_"), is_admin=True)
def handle_user_profile_view(call: CallbackQuery):
    user_id = int(call.data.split("_")[1])

    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_user(user_id)
    if not user:
        bot.answer_callback_query(call.id, "❌ کاربر یافت نشد.", show_alert=True)
        return

    profile_text = get_message(
        "user.profile",
        user_id=user.userid,
        username=user.username,
        balance=user.balance,
        score=user.score
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ افزایش موجودی", callback_data=f"inc_balance_{user.userid}"),
        InlineKeyboardButton("➖ کاهش موجودی", callback_data=f"dec_balance_{user.userid}"),
        InlineKeyboardButton("➕ افزایش امتیاز", callback_data=f"inc_score_{user.userid}"),
        InlineKeyboardButton("➖ کاهش امتیاز", callback_data=f"dec_score_{user.userid}"),
        InlineKeyboardButton("✉️ ارسال پیام", callback_data=f"send_msg_{user.userid}"),
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=profile_text,
        parse_mode="HTML",
        reply_markup=markup
    )

