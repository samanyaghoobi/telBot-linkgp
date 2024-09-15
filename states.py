from telebot.handler_backends import State,StatesGroup


class admin_state(StatesGroup): 
    message_to_all = State()
    deny_reason=State()
    find_user=State()
    increase_balance=State()
    decrease_balance=State()
    increase_score=State()
    decrease_score=State()
    change_banner=State()
    change_amount_pic=State()
    change_cart_name=State()
    change_cart_number=State()
    change_cart_bank_name=State()
class user_state(StatesGroup): 
    pic_receipt = State()
    plan= State()

class banner_state(StatesGroup):
    name=State()
    member=State()
    description=State()
    link=State()
    banner=State()
    week_reserve_get_banner=State()