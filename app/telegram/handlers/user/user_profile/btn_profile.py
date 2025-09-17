from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.telegram.states.banner_state import EditBannerStates
from app.utils.markup.banner_list import build_user_banner_list_markup
from app.utils.message import get_message
from database.session import SessionLocal
from database.repository.banner_repository import BannerRepository
from database.repository.user_repository import UserRepository
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from database.session import SessionLocal
from database.models.banner import Banner
from database.services.banner_service import soft_delete_banner_transaction

@bot.message_handler(func=lambda m: m.text == get_message("btn.user.profile"))
@catch_errors(bot)
def profile_info(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_or_create_user(msg.from_user.id, msg.from_user.username)

        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(get_message("user.balanceIncrease"), callback_data=get_message("user.balanceIncrease")),
            InlineKeyboardButton(get_message("btn.user.convert_points"), callback_data=get_message("btn.user.convert_points")),
            row_width=2
        )

        bot.send_message(
            msg.chat.id,
            text=get_message("user.profile", user_id=user.userid, username=user.username, balance=user.balance, score=user.score),
            parse_mode="HTML",
            reply_markup=markup
        )
    finally:
        db.close()
