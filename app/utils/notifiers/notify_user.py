from telebot import TeleBot

from database.repository.bot_setting_repository import BotSettingRepository
from database.session import SessionLocal
# Step 4: Send admin card info
def send_card_info_to_user(bot: TeleBot, chat_id: int, amount, edit: bool = False, msg_id: int = 0):
       db = SessionLocal()
       try:
              setting_repo = BotSettingRepository(db)

              card_number = setting_repo.bot_setting_get("CART_NUMBER", "6219861934279083")
              bank = setting_repo.bot_setting_get("CART_BANK", "بلو")
              name = setting_repo.bot_setting_get("CART_NAME", "سامان یعقوبی")

              text = (
                     f"💳 <b>اطلاعات واریز برای مبلغ {int(amount):,} تومان:</b>\n\n"
                     f"🔢 <b>شماره کارت :</b> <code>{card_number}</code>\n"
                     f"🏦 <b>بانک            :</b> {bank}\n"
                     f"👤 <b>نام دارنده    :</b> {name}\n\n"
                     f"💬 <i>لطفاً رسید واریز را در پاسخ به همین پیام ارسال نمایید.</i>"
              )

              if edit:
                     bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=text, parse_mode="HTML")
              else:
                     bot.send_message(chat_id, text, parse_mode="HTML")
       finally:
              db.close()
