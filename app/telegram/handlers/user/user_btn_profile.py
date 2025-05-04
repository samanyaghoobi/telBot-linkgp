from app.telegram.bot_instance import bot
from app.telegram.middlewares import check_membership
from app.utils.messages import get_message
from database.base import SessionLocal
from database.repository.user_repository import UserRepository

@bot.message_handler(func=lambda m:m.text == get_message("btn.profile"))
def profile_info(message):
    # if not check_membership(message): return
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_or_create_user(message.from_user.id, message.from_user.username)
    bot.send_message(
        message.chat.id,
        text = get_message("user.profile", user_id=user.userid, username=user.username, balance=user.balance, score=user.score),
        parse_mode="HTML"
    )