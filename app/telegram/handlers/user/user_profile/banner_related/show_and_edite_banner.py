from app.telegram.bot_instance import bot
from telebot.types import CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton,Message
from app.telegram.handlers.other.exception_handler import catch_errors
from app.telegram.states.banner_state import EditBannerStates
from app.utils.markup.banner_list import build_user_banner_list_markup
from database.session import SessionLocal
from database.models.banner import Banner
from database.repository.banner_repository import BannerRepository
from database.repository.user_repository import UserRepository
from database.services.banner_service import soft_delete_banner_transaction
#* show banner
@bot.callback_query_handler(func=lambda c: c.data == "user_show_banners")
@catch_errors(bot)
def show_user_banners(call: CallbackQuery):
    db = SessionLocal()
    repo = UserRepository(db)
    user = repo.get_user(call.from_user.id)

    if not user:
        bot.answer_callback_query(call.id, "شما هیچ بنری ثبت نکرده‌اید.")
        return



    markup = build_user_banner_list_markup(user_id=user.userid)
    text = "📋 لیست بنرهای شما:"
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )


#* banner info
@bot.callback_query_handler(func=lambda c: c.data.startswith("getBanner_"))
@catch_errors(bot)
def show_banner_detail(call: CallbackQuery):
    banner_id = int(call.data.replace("getBanner_", ""))
    db = SessionLocal()
    repo=BannerRepository(db)
    banner = repo.get_by_id(banner_id)

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
@catch_errors(bot)
def delete_banner(call: CallbackQuery):
    banner_id = int(call.data.replace("delete_banner_", ""))
    db = SessionLocal()
    bannerRepo=BannerRepository(db)
    
    banner = bannerRepo.get_by_id(banner_id)
    
    result = soft_delete_banner_transaction(banner_id=banner_id,db=db,user_id=call.message.chat.id,)
    if result:
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
        banner_msg=bot.send_message(call.message.chat.id,banner.text)
        bot.send_message(call.message.chat.id, "✅این بنر با موفقیت حذف شد.",reply_to_message_id=banner_msg.id)
    else:
        bot.answer_callback_query(call.id, "⛔ شما اجازه حذف این بنر را ندارید.")

# @bot.callback_query_handler(func=lambda c: c.data.startswith("edit_banner_"))
# @catch_errors(bot)
# def edit_banner(call: CallbackQuery):
#     text=get_message("error.not.finished")  
#     #todo
#     bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=text)
#     return
    # banner_id = int(call.data.replace("edit_banner_", ""))
    # db = SessionLocal()
    # banner = db.query(Banner).filter_by(id=banner_id).first()

    # if banner and banner.user_id == call.from_user.id:
    #     bot.set_state(call.from_user.id, EditBannerStates.waiting_for_new_banner, call.message.chat.id)
    #     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
    #         data["banner_id"] = banner_id
    #     bot.send_message(call.message.chat.id, "📝 متن جدید بنر را وارد کنید:")
    # else:
    #     bot.answer_callback_query(call.id, "⛔ شما اجازه ویرایش این بنر را ندارید.")

@bot.message_handler(state=EditBannerStates.waiting_for_new_banner)
@catch_errors(bot)
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

