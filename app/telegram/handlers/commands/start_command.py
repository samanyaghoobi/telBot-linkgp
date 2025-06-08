from app.telegram.bot_instance import bot
from app.telegram.middlewares.check_membership import check_membership
from app.utils.command_menu import set_command_menu
from app.utils.keyboard import admin_main_keyboard, user_main_keyboard
from app.utils.message import get_message
from database.repository.user_repository import UserRepository
from database.services.user_service import create_user_if_not_exists
from database.session import SessionLocal

# Handler for admin users

@bot.message_handler(commands=["start","admin"], is_admin=True)
def start_admin(message):
    if not check_membership(message): return
    set_command_menu(message.chat.id)

    bot.send_message(
        message.chat.id,
        get_message("admin.panel"),
        reply_markup=admin_main_keyboard()
    )

# Handler for normal users
@bot.message_handler(commands=["start", "user"])
def start_user(message):
    if not check_membership(message):
        return


    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_or_create_user(message .from_user.id, message .from_user.username)


    bot.send_message(
        message.chat.id,
        get_message("start.welcome"),
        reply_markup=user_main_keyboard()
    )