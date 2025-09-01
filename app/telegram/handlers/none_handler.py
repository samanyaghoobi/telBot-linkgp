from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery,Message

from app.telegram.exception_handler import catch_errors




@bot.callback_query_handler(func=lambda c: c.data == "none")
@catch_errors(bot)
def unimplemented_button(call: CallbackQuery):
    bot.answer_callback_query(call.id, text="❗ این دکمه هنوز فعال نشده.", show_alert=False)


@bot.callback_query_handler(func=lambda c: c.data == "cancel")
@catch_errors(bot)
def unimplemented_button(call: CallbackQuery):
    bot.delete_message(call.message.chat.id,call.message.id)
    bot.delete_state(call.message.from_user.id, call.message.chat.id)

    bot.answer_callback_query(call.id, text="❗ حله عملیات کنسل شد", show_alert=False)



@bot.message_handler(func=lambda m: bot.get_state(m.from_user.id, m.chat.id) is None)
@catch_errors(bot)
def fallback_message_handler(msg: Message):
    bot.send_message(msg.chat.id, "❓ این پیام توسط ربات شناسایی نشد.")

@bot.callback_query_handler(func=lambda c: True)
@catch_errors(bot)
def unknown_callback(call: CallbackQuery):
    bot.answer_callback_query(call.id, text="❓ این عملیات تعریف نشده.", show_alert=False)