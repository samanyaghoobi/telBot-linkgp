from telebot.handler_backends import State,StatesGroup


class admin_state(StatesGroup): 
    message_to_all = State()
    deny_reason=State()
    find_user=State()

class user_state(StatesGroup): 
    pic_receipt = State()
    plan= State()

class banner_state(StatesGroup):
    name=State()
    member=State()
    description=State()
    link=State()
    banner=State()