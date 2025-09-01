from telebot.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from app.utils.message import get_message

def user_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Returns the main menu keyboard for normal users.
    Button labels come from message templates.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(get_message("btn.user.free_times")),
        KeyboardButton(get_message("btn.user.my_reservations")),
        KeyboardButton(get_message("btn.user.profile")),
        KeyboardButton(get_message("btn.user.see_banners")),
        KeyboardButton(get_message("btn.user.rules")),
        KeyboardButton(get_message("btn.user.support"))
    )
    return markup

def admin_main_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(get_message("btn.admin.bot_setting")),
        KeyboardButton(get_message("btn.admin.reservation")),
        KeyboardButton(get_message("btn.admin.user_list")),
        KeyboardButton(get_message("btn.admin.income")),
    )
    return markup

def cancel_markup()->InlineKeyboardMarkup :
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("کنسل کردن" , callback_data="cancel"),
    )
    return markup