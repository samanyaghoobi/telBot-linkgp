from telebot.custom_filters import AdvancedCustomFilter
from telebot import types
from config import ADMINS

class IsAdminFilter(AdvancedCustomFilter):
    key = 'is_admin'  # Used in handler decorators: is_admin=True

    def check(self, message, value):
        # Check for both messages and callback queries
        user_id = (
            message.from_user.id if isinstance(message, types.CallbackQuery)
            else message.from_user.id if hasattr(message, "from_user")
            else message.chat.id
        )
        return user_id in ADMINS
