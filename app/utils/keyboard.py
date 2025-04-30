from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from app.utils.messages import get_message

def user_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Returns the main menu keyboard for normal users.
    Button labels come from message templates.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(get_message("btn.free_times")),
        KeyboardButton(get_message("btn.my_reservations")),
        KeyboardButton(get_message("btn.convert_points")),
        KeyboardButton(get_message("btn.profile")),
        KeyboardButton(get_message("btn.banner")),
        KeyboardButton(get_message("btn.support"))
    )
    return markup

def admin_main_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(get_message("btn.admin.bot_setting")),
        KeyboardButton(get_message("btn.admin.free_time")),
        KeyboardButton(get_message("btn.admin.user_list")),
        KeyboardButton(get_message("btn.admin.income")),
    )
    return markup
