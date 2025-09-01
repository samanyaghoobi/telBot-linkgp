from telebot.handler_backends import StatesGroup, State


class SettingStates(StatesGroup):
    waiting_for_new_value = State()
    waiting_for_setting_key = State()
    waiting_for_setting_value = State()
