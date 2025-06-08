from telebot.types import  InlineKeyboardMarkup,InlineKeyboardButton

from app.utils.message import get_message
from database.models.user import User


def create_pagination_for_users(users_list: list[User], page: int, per_page: int = 10):
    keyboard =  InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(get_message("btn.find_user"),callback_data=get_message("btn.find_user")))
    if len(users_list) <1 :
        button= InlineKeyboardButton(f"هیچ کاربری جهت نمایش وجود ندارد")
        keyboard.add(button)
        return keyboard
    start = page * per_page
    end = start + per_page
    users_in_page = users_list[start:end]

    for user  in users_in_page:
        button =  InlineKeyboardButton(f"{user.username}:{user.userid}", callback_data=f"users_{user.userid}")
        keyboard.add(button)

    nav_buttons = []
    if page > 0:
        nav_buttons.append( InlineKeyboardButton("⬅️ قبلی", callback_data=f'prev_{page-1}'))
    if end < len(users_list):
        nav_buttons.append( InlineKeyboardButton("➡️ بعدی", callback_data=f'next_{page+1}'))
    
    keyboard.row(*nav_buttons)
    
    return keyboard