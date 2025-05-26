from telebot import TeleBot

from database.repository.bot_setting_repository import BotSettingRepository
from database.session import SessionLocal
# Step 4: Send admin card info
def send_card_info_to_user(bot :TeleBot,chat_id: int, amount):
    db = SessionLocal()
    setting_repo = BotSettingRepository(db)

    card_number = setting_repo.bot_setting_get("admin_card_number", "6219861934279083")
    bank = setting_repo.bot_setting_get("admin_card_bank", "بلو")
    name = setting_repo.bot_setting_get("admin_card_holder", "سامان یعقوبی")

    text = f"💳 اطلاعات واریز برای مبلغ {int(amount):,} تومان:\n" \
           f"شماره کارت: <code>{card_number}</code>\nبانک: {bank}\nنام دارنده: {name}\n\n" \
           f"لطفاً رسید واریز را در پاسخ به همین پیام ارسال نمایید."

    bot.send_message(chat_id, text, parse_mode="HTML")
