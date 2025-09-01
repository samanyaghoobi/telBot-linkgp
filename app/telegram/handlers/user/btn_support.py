from telebot.types import Message 
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


SUPPORT_ID = 345490618
SUPPORT_USERNAME = "@linkgp_admin"
SUPPORT_TEXT = "برای ارتباط با پشتیبان روی دکمه زیر کلیک کنید"

@bot.message_handler(func=lambda m: m.text == get_message("btn.user.support"))
@catch_errors(bot)
def support_handler(msg: Message):
    bot.delete_state(user_id=msg.from_user.id, chat_id=msg.chat.id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 پشتیبان", url=f"https://t.me/{SUPPORT_USERNAME.lstrip('@')}",))

    bot.send_message(
        chat_id=msg.chat.id,
        text=SUPPORT_TEXT,
        reply_markup=markup,
        parse_mode="HTML"
    )

