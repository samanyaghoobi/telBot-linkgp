from telebot.handler_backends import State,StatesGroup


class admin_state(StatesGroup): 

    message_to_all = State()
    find_user=State()
    change_banner=State()
    #financial
    deny_reason=State()
    increase_balance=State()
    decrease_balance=State()
    increase_score=State()
    decrease_score=State()
    change_amount_pic=State()
    #card info
    change_cart_name=State()
    change_cart_number=State()
    change_cart_bank_name=State()
    #price
    change_price_min=State()
    change_price_mid=State()
    change_price_max=State()
    
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