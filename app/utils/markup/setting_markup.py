from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.message import get_message
from database.models.bot_setting import BotSetting


def make_setting_markup(settings :list[BotSetting])-> InlineKeyboardMarkup:
    markup= InlineKeyboardMarkup()
    
    btn=InlineKeyboardButton(get_message("btn.admin.get_backup"),callback_data=get_message("btn.admin.get_backup"))
    markup.add(btn)
    if len(settings)<1 : 
        btn=InlineKeyboardButton(get_message("btn.noOption"),callback_data=f"!!!")
        markup.add(btn)

    for setting in settings:
        btn=InlineKeyboardButton(f"{setting.key}:{setting.value}",callback_data=f"botSetting_{setting.key}")
        markup.add(btn)
    return markup        