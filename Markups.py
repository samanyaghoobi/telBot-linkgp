from configs.config import * 
from functions.custom_functions import *
from message_and_text.text import *
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery

########################################################################
back_button=InlineKeyboardButton(text="back",callback_data="back")
#markups
markup_join=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
markup_join.add(button)
###!user
markup_main=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
markup_main.add(free_rime_btn)
markup_main.add(user_find_reserve)
markup_main.add(user_account_btn,user_find_reserve)
markup_main.add(support_btn,make_banner_btn)
###!admin
markup_main_admin=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
markup_main_admin.add(free_rime_btn,admin_btn_bot_info)
markup_main_admin.add(admin_btn_reserves)
markup_main_admin.add(admin_btn_user_list,admin_btn_find_user_info)
markup_main_admin.add(admin_btn_send_msg_to_all,admin_btn_check_income)

def make_admin_markup_user_info():
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=admin_btn_increase_balance,callback_data=admin_btn_increase_balance)
    btn2=InlineKeyboardButton(text=admin_btn_decrease_balance,callback_data=admin_btn_decrease_balance)
    btn3=InlineKeyboardButton(text=admin_btn_increase_score,callback_data=admin_btn_increase_score)
    btn4=InlineKeyboardButton(text=admin_btn_decrease_score,callback_data=admin_btn_decrease_score)
    btn5=InlineKeyboardButton(text=admin_btn_msg_user,callback_data=admin_btn_msg_user)
    btn6=InlineKeyboardButton(text=admin_btn_delete_user,callback_data=admin_btn_delete_user)
    markup.add(btn1,btn2)
    markup.add(btn3,btn4)
    markup.add(btn5,btn6)
    return markup