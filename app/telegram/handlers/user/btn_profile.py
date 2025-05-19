from app.telegram.bot_instance import bot
from app.telegram.states.baner_state import EditBannerStates
from app.utils.markup.banner_list import build_user_banner_list_markup
from app.utils.messages import get_message
from database.base import SessionLocal
from database.repository.user_repository import UserRepository
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.utils.messages import get_message
from database.base import SessionLocal
from database.models.banner import Banner

@bot.message_handler(func=lambda m:m.text == get_message("btn.profile"))
def profile_info(message):
    # if not check_membership(message): return
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_or_create_user(message.from_user.id, message.from_user.username)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(get_message("btn.user.charge"), callback_data="user_charge"),
        InlineKeyboardButton(get_message("btn.user.show_banners"), callback_data="user_show_banners")
    )

    bot.send_message(
        message.chat.id,
        text=get_message("user.profile", user_id=user.userid, username=user.username, balance=user.balance, score=user.score),
        parse_mode="HTML",
        reply_markup=markup
    )

#* show banner
@bot.callback_query_handler(func=lambda c: c.data == "user_show_banners")
def show_user_banners(call: CallbackQuery):
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_user(call.from_user.id)

    if not user or not user.banners:
        bot.answer_callback_query(call.id, "شما هیچ بنری ثبت نکرده‌اید.")
        return

    markup = build_user_banner_list_markup(user.banners)
    text="📋 لیست بنرهای شما:"
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text,reply_markup=markup)


#* banner info
@bot.callback_query_handler(func=lambda c: c.data.startswith("getBanner_"))
def show_banner_detail(call: CallbackQuery):
    banner_id = int(call.data.replace("banner_", ""))
    db = SessionLocal()
    banner = db.query(Banner).filter_by(id=banner_id).first()

    if not banner or banner.user_id != call.from_user.id:
        bot.answer_callback_query(call.id, "بنر یافت نشد یا مجاز نیستید.")
        return

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("🗑 حذف", callback_data=f"delete_banner_{banner.id}"),
        InlineKeyboardButton("✏️ ویرایش", callback_data=f"edit_banner_{banner.id}")
    )
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=banner.text,reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("delete_banner_"))
def delete_banner(call: CallbackQuery):
    banner_id = int(call.data.replace("delete_banner_", ""))
    db = SessionLocal()
    banner = db.query(Banner).filter_by(id=banner_id).first()

    if banner and banner.user_id == call.from_user.id:
        db.delete(banner)
        db.commit()
        bot.answer_callback_query(call.id, "بنر حذف شد.")
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
        bot.send_message(call.message.chat.id, "✅ بنر با موفقیت حذف شد.")
    else:
        bot.answer_callback_query(call.id, "⛔ شما اجازه حذف این بنر را ندارید.")

@bot.callback_query_handler(func=lambda c: c.data.startswith("edit_banner_"))
def edit_banner(call: CallbackQuery):
    text=get_message("error.not.finished")
    print('tser')
    print("hi")
    #todo
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)
    return
    banner_id = int(call.data.replace("edit_banner_", ""))
    db = SessionLocal()
    banner = db.query(Banner).filter_by(id=banner_id).first()

    if banner and banner.user_id == call.from_user.id:
        bot.set_state(call.from_user.id, EditBannerStates.waiting_for_new_banner, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data["banner_id"] = banner_id
        bot.send_message(call.message.chat.id, "📝 متن جدید بنر را وارد کنید:")
    else:
        bot.answer_callback_query(call.id, "⛔ شما اجازه ویرایش این بنر را ندارید.")

@bot.message_handler(state=EditBannerStates.waiting_for_new_banner)
def update_banner_text(msg: Message):
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        banner_id = data.get("banner_id")

    db = SessionLocal()
    banner = db.query(Banner).filter_by(id=banner_id).first()

    if banner and banner.user_id == msg.from_user.id:
        banner.text = msg.text
        db.commit()
        bot.send_message(msg.chat.id, "✅ بنر با موفقیت ویرایش شد:")
        bot.send_message(msg.chat.id, msg.text)
    else:
        bot.send_message(msg.chat.id, "⛔ امکان ویرایش وجود ندارد.")

    bot.delete_state(msg.from_user.id, msg.chat.id)

######################################################################
#* charge acc
@bot.callback_query_handler(func=lambda c: c.data == "user_charge")
def user_charge_handler(call: CallbackQuery):
    bot.send_message(call.message.chat.id, get_message("user.charge.instructions"))
