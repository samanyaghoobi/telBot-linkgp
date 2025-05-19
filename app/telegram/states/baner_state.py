from telebot.handler_backends import StatesGroup, State



class BannerStates(StatesGroup):

    waiting_for_title = State()
    waiting_for_name = State()
    waiting_for_member = State()
    waiting_for_link = State()


    
class EditBannerStates(StatesGroup):
    waiting_for_new_banner = State()