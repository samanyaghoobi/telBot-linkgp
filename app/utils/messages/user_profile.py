from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models.user import User
from app.utils.message import get_message


def get_userProfile_and_markup( user: User ) -> tuple:
    """return profile_text, markup"""
    # Prepare the profile text using the user data
    profile_text = get_message(
        "user.profile",
        user_id=user.userid,
        username=user.username,
        balance=user.balance,
        score=user.score
    )

    # Create the inline keyboard markup
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("➕ افزایش موجودی", callback_data=f"inc_balance_{user.userid}"),
        InlineKeyboardButton("➖ کاهش موجودی", callback_data=f"dec_balance_{user.userid}"),
        InlineKeyboardButton("➕ افزایش امتیاز", callback_data=f"inc_score_{user.userid}"),
        InlineKeyboardButton("➖ کاهش امتیاز", callback_data=f"dec_score_{user.userid}"),
        InlineKeyboardButton("✉️ ارسال پیام", callback_data=f"send_msg_{user.userid}"),
    )

    # Return both profile text and markup
    return profile_text, markup
