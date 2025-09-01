from telebot.handler_backends import State, StatesGroup

class AdminUserEditState(StatesGroup):
    waiting_for_amount = State()
    waiting_for_message = State()
