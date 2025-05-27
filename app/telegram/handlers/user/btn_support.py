from telebot.types import Message 
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message

SUPPORT_ID=345490618
support_msg=f"""<a href='tg://user?id={SUPPORT_ID}'> برا ارتباط با پشتیبان لطفا روی این متن کلیک کنید </a>"""

#markup support btn

@bot.message_handler(func=lambda m:m.text == get_message("btn.support"))
@catch_errors(bot)
def account(msg : Message):
    bot.delete_state(user_id= msg.from_user.id,chat_id=msg.chat.id)
    bot.send_message(chat_id=msg.chat.id,text=support_msg,parse_mode="HTML")