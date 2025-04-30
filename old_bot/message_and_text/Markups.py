from configs.basic_info import * 
from functions.custom_functions import *
from telebot.types import InlineKeyboardButton ,InlineKeyboardMarkup,ReplyKeyboardMarkup,KeyboardButton,Message,CallbackQuery
from message_and_text.bot_messages import *
from message_and_text.markup_text import *
########################################################################



back_button=InlineKeyboardButton(text="back",callback_data="back")
#markups
markup_join=InlineKeyboardMarkup()
button=InlineKeyboardButton(text="برسی عضویت",callback_data="proceed")
markup_join.add(button)
###!user
markup_user_main=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
markup_user_main.add(markup_user_free_rime)
markup_user_main.add(markup_user_find_reserve)
markup_user_main.add(markup_user_account_btn,btn_convert_score)
markup_user_main.add(btn_support,markup_user_make_banner)


###!admin
markup_main_admin=ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
markup_main_admin.add(markup_user_free_rime,markup_admin_bot_setting)
markup_main_admin.add(markup_admin_reserves)
markup_main_admin.add(markup_admin_user_list,markup_admin_find_user_info)
markup_main_admin.add(markup_admin_send_msg_to_all,markup_admin_check_income)

def markup_make_admin_user_info():
    markup=InlineKeyboardMarkup()
    btn1=InlineKeyboardButton(text=markup_admin_increase_balance,callback_data=markup_admin_increase_balance)
    btn2=InlineKeyboardButton(text=markup_admin_decrease_balance,callback_data=markup_admin_decrease_balance)
    btn3=InlineKeyboardButton(text=markup_admin_increase_score,callback_data=markup_admin_increase_score)
    btn4=InlineKeyboardButton(text=markup_admin_decrease_score,callback_data=markup_admin_decrease_score)
    btn5=InlineKeyboardButton(text=markup_admin_msg_user,callback_data=markup_admin_msg_user)
    btn6=InlineKeyboardButton(text=markup_admin_delete_user,callback_data=markup_admin_delete_user)
    markup.add(btn1,btn2)
    markup.add(btn3,btn4)
    markup.add(btn5,btn6)
    return markup

def markup_bot_setting(bot_is_enable:bool=True):
    markup=InlineKeyboardMarkup()
    change_card_number=InlineKeyboardButton(text=markup_admin_bot_setting_change_cart,callback_data=markup_admin_bot_setting_change_cart)
    # restart_bot=InlineKeyboardButton(text=markup_admin_bot_setting_restart_bot,callback_data=markup_admin_bot_setting_restart_bot)
    text_bot_is_enable="فعال ✅" if bot_is_enable else "غیرفعال ❌"
    btn_enable_disable=InlineKeyboardButton(text=f"🤖 ربات {text_bot_is_enable}",callback_data=f"change_bot_enable_disable")

    change_price=InlineKeyboardButton(text=markup_admin_bot_setting_change_price,callback_data=markup_admin_bot_setting_change_price)

    markup.add(change_card_number)
    markup.add(change_price)
    markup.add(btn_enable_disable)
    # markup.add(restart_bot)
    return markup

    