from telebot import  types

from database.models.user import User


def create_pagination_for_users(users_list: list[User], page: int, per_page: int = 10):
    keyboard = types.InlineKeyboardMarkup()
    if len(users_list) <1 :
        button=types.InlineKeyboardButton(f"هیچ کاربری جهت نمایش وجود ندارد")
        keyboard.add(button)
        return keyboard
    start = page * per_page
    end = start + per_page
    users_in_page = users_list[start:end]

    for user  in users_in_page:
        button = types.InlineKeyboardButton(f"{user.username}:{user.userid}", callback_data=f"users_{user.userid}")
        keyboard.add(button)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton("⬅️ قبلی", callback_data=f'prev_{page-1}'))
    if end < len(users_list):
        nav_buttons.append(types.InlineKeyboardButton("➡️ بعدی", callback_data=f'next_{page+1}'))
    
    keyboard.row(*nav_buttons)
    
    return keyboard