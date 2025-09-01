from telebot.types import Message
from app.telegram.bot_instance import bot
from config import MANDATORY_CHANNELS
from app.utils.message import get_message

def is_user_member(user_id: int, channel_username: str) -> bool:
    """
    Checks if the user is a member of a specific channel.
    """
    try:
        member = bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

def check_membership(message: Message) -> bool:
    return True # todo 
    """
    Validates user membership across all required channels.
    If not a member, sends a warning and returns False.
    """
    for channel in MANDATORY_CHANNELS:
        if not is_user_member(message.from_user.id, channel):
            bot.send_message(
                message.chat.id,
                get_message("error.not_member", channel=channel)
            )
            return False
    return True
