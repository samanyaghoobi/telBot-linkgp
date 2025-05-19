from telebot.types import Message,CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.states.setting_state import SettingStates
from app.utils.markup.setting_markup import make_setting_markup
from app.utils.messages import get_message
from database.base import SessionLocal
from database.repository.bot_setting_repository import BotSettingRepository

@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.bot_setting"), is_admin=True)
def show_settings(msg: Message):
    db = SessionLocal()
    repo =BotSettingRepository(db)  
    settings=repo.get_all_settings()
    markup= make_setting_markup(settings)      

    bot.send_message(msg.chat.id, get_message("msg.admin.setting"), parse_mode="Markdown",reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("botSetting_"),is_admin=True)
def ask_new_setting_value(call: CallbackQuery):
    key = call.data.replace("botSetting_", "")
    db = SessionLocal()
    repo = BotSettingRepository(db)
    value = repo.bot_setting_get(key)

    bot.send_message(
        call.message.chat.id,
        f"🔧 تنظیم فعلی: `{key} = {value}`\nمقدار جدید را ارسال کنید:",
        parse_mode="Markdown")
    bot.set_state(state=SettingStates.waiting_for_new_value,user_id=call.message.chat.id,chat_id=call.message.chat.id)
    with bot.retrieve_data(call.message.chat.id, call.message.chat.id) as data:
        data['key'] = key
    print("hi")





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
