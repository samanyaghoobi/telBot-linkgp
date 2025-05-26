from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
from app.telegram.states.user_state import userState
from app.utils.notifiers.notify_user import send_card_info_to_user
# Step 3: Enter custom amount
@bot.message_handler(state=userState.waiting_for_inc_amount)
@catch_errors(bot)
def handle_custom_amount(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, "❌ لطفاً فقط عدد وارد کنید.")
        return

    amount = int(msg.text)

    if not (1 <= amount <= 1000):
        bot.send_message(msg.chat.id, "❌ مبلغ باید بین 1 تا 1000 (هزار تومان تا یک میلیون تومان) باشد.")
        return
    
    # Store amount in state data
    bot.set_state(state=userState.waiting_for_pic,user_id=msg.chat.id,chat_id=msg.chat.id)
    with bot.retrieve_data(user_id=msg.chat.id , chat_id=msg.chat.id) as data:
        data["amount"]=amount
    send_card_info_to_user(bot,msg.chat.id, amount)