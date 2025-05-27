from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,Message
from database.models.user import User
from telebot import TeleBot
from app.utils.message import get_message

def show_user_profile_to_admin(bot:TeleBot, chat_id:int, user:User, reply_to_message_id=None)->Message:
    profile_text = get_message(
        "user.profile",
        user_id=user.userid,
        username=user.username,
        balance=user.balance,
        score=user.score
    )

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ افزایش موجودی", callback_data=f"inc_balance_{user.userid}"),
        InlineKeyboardButton("➖ کاهش موجودی", callback_data=f"dec_balance_{user.userid}"),
        InlineKeyboardButton("➕ افزایش امتیاز", callback_data=f"inc_score_{user.userid}"),
        InlineKeyboardButton("➖ کاهش امتیاز", callback_data=f"dec_score_{user.userid}"),
        InlineKeyboardButton("✉️ ارسال پیام", callback_data=f"send_msg_{user.userid}"),
    )

    message :Message= bot.send_message(
        chat_id=chat_id,
        text=profile_text,
        parse_mode="HTML",
        reply_to_message_id=reply_to_message_id,
        reply_markup=markup
    )
    return message
