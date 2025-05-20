#* charge acc
from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery
from app.telegram.handlers.other.exception_handler import catch_errors
from app.utils.messages import get_message
#* charge acc
# @bot.callback_query_handler(func=lambda c: c.data == "user_charge")
# @catch_errors(bot)
# def user_charge_handler(call: CallbackQuery):
#     bot.send_message(call.message.chat.id, get_message("user.charge.instructions"))
