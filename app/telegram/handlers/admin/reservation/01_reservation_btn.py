from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
from app.utils.messages import get_message
from config import ADMINS  # لیست آی‌دی ادمین‌ها

@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.reservation") , is_admin=True)
@catch_errors(bot)
def admin_reservation_menu(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📅 فقط رزروهای امروز به بعد", callback_data="admin_reserve_upcoming"),
        InlineKeyboardButton("📖 مشاهده همه رزروها", callback_data="admin_reserve_all_dates")
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=markup
    )
