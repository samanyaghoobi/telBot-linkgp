from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.telegram.middlewares.check_membership import check_membership
from app.utils.command_menu import set_command_menu
from app.utils.keyboard import admin_main_keyboard, user_main_keyboard
from app.utils.message import get_message
from database.repository.user_repository import UserRepository
from database.services.user_service import create_user_if_not_exists
from database.session import SessionLocal
from app.telegram.scheduled.banner_publisher import publish_custom_banner

# Handler for admin users

@bot.message_handler(commands=["start","admin"], is_admin=True)
@catch_errors(bot)
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
@catch_errors(bot)
def start_user(message):
    if not check_membership(message):
        return

    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_or_create_user(message.from_user.id, message.from_user.username)
        bot.send_message(
            message.chat.id,
            get_message("start.welcome"),
            reply_markup=user_main_keyboard()
        )
    finally:
        db.close()

@bot.message_handler(commands=["test"], is_admin=True)
def test_publish_custom_banner(message):
    test_text = "این یک پیام تستی است که توسط ادمین ارسال شده است."
    banner_title = "بنر تستی"
    publish_custom_banner(test_text, banner_title)
    bot.reply_to(message, "پیام تستی به کانال و ادمین‌ها ارسال شد.")
