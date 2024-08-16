from telebot.handler_backends import State,StatesGroup


class admin_state(StatesGroup): 
    message_to_all = State()
    deny_reason=State()
    find_user=State()
    increase_balance=State()
    decrease_balance=State()
    increase_score=State()
    decrease_score=State()

class user_state(StatesGroup): 
    pic_receipt = State()
    plan= State()

class banner_state(StatesGroup):
    name=State()
    member=State()
    description=State()
    link=State()
    banner=State()