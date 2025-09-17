
from app.telegram.bot_instance import bot
from telebot.types import Message,CallbackQuery
from app.utils.message import get_message
from app.utils.messages.user_profile import get_userProfile_and_markup
from app.utils.regex.user_id_finder import extract_user_id
from database.repository.user_repository import UserRepository
from database.session import SessionLocal
#find userAuto
@bot.message_handler(
    is_admin=True,
    content_types=["text", "forward_from"],
    func=lambda m: (
        bot.get_state(m.from_user.id, m.chat.id) is None and (
            m.forward_from is not None or
            (m.text and m.text.strip().isdigit()) or
            (m.text and extract_user_id(m.text) is not None)  # Added check for formatted user ID
        )
    )
)
def search_user_by_forward_or_id(msg: Message):
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user_id = None

        if msg.text and msg.text.strip().isdigit():
            user_id = int(msg.text.strip())
        elif msg.text:
            user_id = extract_user_id(msg.text)

        user = repo.get_user(user_id)
        if user:
            profile_text, markup = get_userProfile_and_markup(user=user)
            bot.send_message(
                chat_id=msg.chat.id,
                text=profile_text,
                parse_mode="HTML",
                reply_markup=markup
            )
        else:
            bot.send_message(msg.chat.id, get_message("error.userNotFound"))
    finally:
        db.close()


@bot.callback_query_handler(func=lambda call: call.data== get_message("btn.find_user"))
def find_user(call: CallbackQuery):
    bot.delete_message(call.message.chat.id,call.message.id)
    bot.send_message(call.message.chat.id,text=get_message("msg.find_user"))