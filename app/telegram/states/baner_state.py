from telebot.handler_backends import StatesGroup, State



class BannerStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_member = State()
    waiting_for_link = State()
