from app.utils.markup.week_markup import show_week_for_navigation
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,Message
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from database.session import SessionLocal
from datetime import  timedelta, date

from app.telegram.exception_handler import catch_errors


# Step 1: Display the list of days from this week (starting from today)

@bot.message_handler(func=lambda m: m.text == get_message("btn.free_times"))
@catch_errors(bot)
def show_week_days(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    today = date.today()
    weekday = (today.weekday() + 2) % 7  #for  start from saturday and end in friday
    start_of_week = today - timedelta(days=weekday)

    text=get_message("msg.select_day")
    # Create the buttons for the days of the week
    markup=InlineKeyboardMarkup(row_width=3)
    markup.add(InlineKeyboardButton(get_message("msg.selectCustomTime"),callback_data="customReservation"))
    markup= show_week_for_navigation(message=text,start_of_week=start_of_week,input_markup=markup)

    bot.send_message(msg.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('week_prev'))
def go_previous_week(call:CallbackQuery):
    # Extract the starting date of the previous week from the callback data
    start_of_week_str = call.data.split('_')[2]
    start_of_week = date.fromisoformat(start_of_week_str)
    prev_week_start = start_of_week - timedelta(days=7)
    markup=show_week_for_navigation(call.message, prev_week_start)
    bot.edit_message_text(text=get_message("msg.select_day"),chat_id=call.message.chat.id,message_id= call.message.id , reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('week_next'))
def go_next_week(call:CallbackQuery):
    # Extract the starting date of the next week from the callback data
    start_of_week_str = call.data.split('_')[2]
    start_of_week = date.fromisoformat(start_of_week_str)
    next_week_start = start_of_week + timedelta(days=7)
    markup=show_week_for_navigation(call.message, next_week_start)
    bot.edit_message_text(text=get_message("msg.select_day"),chat_id=call.message.chat.id,message_id= call.message.id , reply_markup=markup)

