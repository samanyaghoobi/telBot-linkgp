from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
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

@bot.message_handler(func=lambda m:m.text == get_message("btn.profile"))
@catch_errors(bot)
def profile_info(message):
    # if not check_membership(message): return
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_or_create_user(message.from_user.id, message.from_user.username)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(get_message("btn.user.charge"), callback_data="user_charge"),
        InlineKeyboardButton(get_message("btn.user.show_banners"), callback_data="user_show_banners"),
        InlineKeyboardButton(get_message("btn.convert_points"), callback_data="convert_points"),
        row_width=2
    )

    bot.send_message(
        message.chat.id,
        text=get_message("user.profile", user_id=user.userid, username=user.username, balance=user.balance, score=user.score),
        parse_mode="HTML",
        reply_markup=markup
    )

