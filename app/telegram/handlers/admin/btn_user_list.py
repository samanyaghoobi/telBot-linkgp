from app.utils.messages import get_message
from app.utils.paging_inline_btn import create_pagination
from app.telegram.bot_instance import bot
from telebot.types import Message
from database.base import SessionLocal
from database.repository.user_repository import UserRepository 


@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.user_list"), is_admin=True)
def user_list(msg: Message):
    
     db = SessionLocal()
     repo = UserRepository(db)
     users = repo.get_all_users()

     markup = create_pagination(users, 0)
     bot.send_message(
          chat_id=msg.chat.id,
          text=get_message("msg.admin.user_list"),
          reply_markup=markup)

from telebot.types import CallbackQuery

@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_") or call.data.startswith("next_"))
def paginate_user_list(call: CallbackQuery):
    db = SessionLocal()
    repo = UserRepository(db)
    users = repo.get_all_users()

    page = int(call.data.split("_")[1])
    markup = create_pagination(users, page)

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
