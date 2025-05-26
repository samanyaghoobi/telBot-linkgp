from telebot.handler_backends import StatesGroup, State


class userState(StatesGroup):
    waiting_for_inc_amount = State()
    waiting_for_pic=State()

# States
class ChargeStates(StatesGroup):
    waiting_for_reject_reason = State()
    waiting_for_edit_amount = State()
