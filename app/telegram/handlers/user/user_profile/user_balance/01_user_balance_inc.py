from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
from app.telegram.states.user_state import userState
from app.utils.message import get_message
from app.utils.notifiers.notify_user import send_card_info_to_user
from config import ADMINS
from database.session import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository
import re

# Step 1: Show predefined charge options
@bot.callback_query_handler(func=lambda c: c.data == "user_charge" )
@catch_errors(bot)
def start_charge_flow(call: CallbackQuery):
    db = SessionLocal()
    setting_repo = BotSettingRepository(db)
    options_str = setting_repo.bot_setting_get("charge_options", "8,15,25")
    options = [int(opt.strip()) for opt in options_str.split(",") if opt.strip().isdigit()]

    markup = InlineKeyboardMarkup(row_width=2)
    for amount in options:
        markup.add(InlineKeyboardButton(f"{amount:,} هزارتومان", callback_data=f"select_charge_{amount}"))
    markup.add(InlineKeyboardButton("💳 مبلغ دلخواه", callback_data="select_charge_custom"))

    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text= "💰 لطفاً یکی از مبالغ زیر را برای شارژ انتخاب کنید:", reply_markup=markup)

# Step 2: Handle charge selection
@bot.callback_query_handler(func=lambda c: c.data.startswith("select_charge_"))
@catch_errors(bot)
def handle_charge_selection(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    selected = call.data.replace("select_charge_", "")

    if selected == "custom":
        bot.edit_message_text(message_id=call.message.id,chat_id=call.message.chat.id, text="لطفاً مبلغ موردنظر خود را (به تومان) وارد کنید:")
        bot.set_state(state=userState.waiting_for_inc_amount,user_id=call.message.chat.id,chat_id=call.message.chat.id)
        
    else:
        send_card_info_to_user(bot,call.message.chat.id, selected,edit=True,msg_id=call.message.id)
        bot.set_state(state=userState.waiting_for_pic,user_id=call.message.chat.id,chat_id=call.message.chat.id)
        with bot.retrieve_data(user_id=call.message.chat.id , chat_id=call.message.chat.id) as data:
            data["amount"]=selected

