from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message,CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from config import ADMINS

class IsAdminFilter(AdvancedCustomFilter):
    key = 'is_admin'  # Used in handler decorators: is_admin=True

    def check(self, message :Message, value):
        # Check for both messages and callback queries
        user_id = (
            message.from_user.id if isinstance(message, CallbackQuery)
            else message.from_user.id if hasattr(message, "from_user")
            else message.chat.id
        )
        return user_id in ADMINS

class NoStateFilter(AdvancedCustomFilter):
    key = 'no_state'

    def check(self, message, value):
        state = bot.get_state(message.from_user.id, message.chat.id)
        return state is None


class is_button(AdvancedCustomFilter):
    key = 'IsNotButton'

    def __init__(self):
        self.allowed_texts = {
            get_message("btn.free_times"),
            get_message("btn.my_reservations"),
            get_message("btn.profile"),
            get_message("btn.user.make_banner"),
            get_message("btn.support"),
            get_message("btn.admin.bot_setting"),
            get_message("btn.admin.reservation"),
            get_message("btn.admin.user_list"),
            get_message("btn.admin.income")
        }

    def check(self, message: Message, value: bool) -> bool:
        is_button =message.text  in self.allowed_texts
        return  not is_button