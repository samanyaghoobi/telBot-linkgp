from telebot.handler_backends import StatesGroup, State


class SettingStates(StatesGroup):
    waiting_for_new_value = State()
