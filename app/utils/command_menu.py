from telebot.types import BotCommandScopeChat
from app.messages.fa import ADMIN_COMMANDS
from app.telegram.bot_instance import bot
from config import ADMINS

def set_command_menu(chat_id: int):
    """
    Sets the command menu for the given chat.
    Chooses between admin/user commands based on user ID.
    """
    command_list = ADMIN_COMMANDS if chat_id in ADMINS else None
    bot.set_my_commands(command_list, scope=BotCommandScopeChat(chat_id))