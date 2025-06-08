from telebot.types import Message,CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.telegram.states.setting_state import SettingStates
from app.utils.markup.setting_markup import make_setting_markup
from app.utils.message import get_message
from database.repository.bot_setting_repository import BotSettingRepository
from database.session import SessionLocal

@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.bot_setting"), is_admin=True)
def show_settings(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    db = SessionLocal()
    repo =BotSettingRepository(db)  
    settings=repo.get_all_settings()
    markup= make_setting_markup(settings)      
    bot.send_message(chat_id=msg.chat.id, text=get_message("msg.admin.setting"),reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("botSetting_"),is_admin=True)
def ask_new_setting_value(call: CallbackQuery):
    key = call.data.replace("botSetting_", "")
    db = SessionLocal()
    repo = BotSettingRepository(db)
    value = repo.bot_setting_get(key)
    bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.id)
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("❌ لغو", callback_data="cancel")
    )
    markup.add(
        InlineKeyboardButton("🗑 حذف", callback_data=f"deleteSetting_{key}")
    )

    bot.send_message(
        call.message.chat.id,
        f"🔧 تنظیم فعلی: `{key} = {value}`\nمقدار جدید را ارسال کنید:",
        parse_mode="Markdown",reply_markup=markup)
    bot.set_state(state=SettingStates.waiting_for_new_value,user_id=call.message.chat.id,chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['key'] = key





@bot.message_handler(state=SettingStates.waiting_for_new_value,is_admin=True)
def receive_new_setting_value(msg: Message):
    with bot.retrieve_data(msg.chat.id, msg.chat.id) as data:
        key=data['key']

    if not key:
        bot.send_message(msg.chat.id, "⛔ خطا: کلید مشخص نیست.")
        return

    db = SessionLocal()
    repo = BotSettingRepository(db)
    repo.bot_setting_set(key, msg.text)

    bot.send_message(msg.chat.id, f"✅ مقدار جدید برای `{key}` ذخیره شد: `{msg.text}`", parse_mode="Markdown")
    bot.delete_state(msg.from_user.id, msg.chat.id)


@bot.callback_query_handler(func=lambda call: call.data == get_message("btn.admin.add_setting"), is_admin=True)
def ask_setting_key(call: CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="❌ لغو", callback_data="cancel"))

    bot.send_message(call.message.chat.id, "📝 لطفاً کلید تنظیم جدید را وارد کنید:",reply_markup=markup)
    bot.set_state(state=SettingStates.waiting_for_setting_key, user_id=call.from_user.id, chat_id=call.message.chat.id)

@bot.message_handler(state=SettingStates.waiting_for_setting_key, is_admin=True)
def receive_setting_key(message: Message):
    key = message.text.strip()
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton(text="❌ لغو", callback_data="cancel"))
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)


    bot.send_message(message.chat.id, f"🔑 کلید تنظیم: `{key}`\nلطفاً مقدار آن را وارد کنید:", parse_mode="Markdown",reply_markup=markup)
    bot.set_state(state=SettingStates.waiting_for_setting_value, user_id=message.from_user.id, chat_id=message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['key'] = key

@bot.message_handler(state=SettingStates.waiting_for_setting_value, is_admin=True)
def receive_setting_value(message: Message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    value = message.text.strip()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        key = data.get('key')

    db = SessionLocal()
    repo = BotSettingRepository(db)
    repo.bot_setting_add(key, value)

    bot.send_message(message.chat.id, f"✅ تنظیم جدید اضافه شد:\n`{key} = {value}`", parse_mode="Markdown")
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("deleteSetting_"), is_admin=True)
def delete_setting_handler(call: CallbackQuery):
    key = call.data.replace("deleteSetting_", "")
    db = SessionLocal()
    repo = BotSettingRepository(db)
    repo.bot_setting_delete(key)
    

    bot.answer_callback_query(call.id, text=f"✅ حذف شد: {key}")
    bot.delete_message(call.message.chat.id, call.message.message_id)

    # نمایش لیست جدید تنظیمات
    settings = repo.get_all_settings()
    markup = make_setting_markup(settings)
    bot.send_message(call.message.chat.id, get_message("msg.admin.setting"), reply_markup=markup)
