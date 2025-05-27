
from app.telegram.bot_instance import bot
from telebot.types import Message
from app.utils.messages.user_profile import show_user_profile_to_admin
from database.repository.user_repository import UserRepository
from database.session import SessionLocal
#find userAutoasdf
@bot.message_handler(
    is_admin=True,
    content_types=["text", "forward_from"],
    func=lambda m: (
        bot.get_state(m.from_user.id, m.chat.id) is None and (
            m.forward_from is not None or
            (m.text and m.text.strip().isdigit())
        )
    )
)
def search_user_by_forward_or_id(msg: Message):
    db = SessionLocal()
    repo = UserRepository(db)

    user_id = None
    if msg.forward_from:
        user_id = msg.forward_from.id
    elif msg.text.isdigit():
        user_id = int(msg.text)

    if not user_id:
        bot.send_message(msg.chat.id, "❌ لطفاً پیام کاربر را فوروارد کنید یا آی‌دی عددی وارد نمایید.")
        return

    user = repo.get_user(user_id)
    if user:
        show_user_profile_to_admin(bot, msg.chat.id, user, reply_to_message_id=msg.message_id)
    else:
        bot.send_message(msg.chat.id, "❌ کاربر یافت نشد.")

