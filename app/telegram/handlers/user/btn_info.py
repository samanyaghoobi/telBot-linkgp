from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message

# متن قوانین و امتیاز (قابل تنظیم از یک فایل یا دیتابیس)
RULES_TEXT = """
📌 <b>قوانین استفاده از ربات:</b>

1. هر لینک تنها یک‌بار در روز مجاز به تبلیغ است.

2. تبلیغ لینک‌های زیر ممنوع و حذف می‌شود:
   - کانال تلگرام
   - محتوای غیراخلاقی
   - فروش کالا
   - لینک‌های اسکم یا مشکوک

3. گزارش باگ همراه با جایزه است ✅

4. لینک‌ها تا زمانی که تلگرام اجازه دهد قابل ویرایش هستند اما تکرار نمی‌شوند.

5. ارسال لینک فقط از طریق ربات و به‌صورت خودکار انجام می‌شود.

6. اگر لینکی ارسال نشد:
   - موضوع را به ادمین گزارش دهید.
   - مبلغ رزرو بازگردانده می‌شود.
   - و ۵۰٪ بیشتر به ربات بازمی‌گردد.

🎁 <b>سیستم امتیازدهی:</b>
- هر رزرو موفق: 1 امتیاز
- 10 امتیاز = 1 رزرو رایگان
- امتیازها قابل فروش یا انتقال نیستند

⚠️ قوانین ممکن است در آینده تغییر کنند.
"""
PLANS="""

🔷 <b>طرح‌های تبلیغاتی:</b>

📌 <b>طرح ۱</b>
- زمان: ۱۳ تا ۱۷
- حداقل نمایش: ۱ ساعت
- 💰 ۸ هزار تومان

📌 <b>طرح ۲</b>
- زمان: ۱۸ تا ۰۱:۳۰
- حداقل نمایش: نیم ساعت
- 💰 ۱۵ هزار تومان

📌 <b>طرح ویژه</b>
- فقط یک لینک در روز
- زمان: ۰۲:۰۰ شب تا ۱۳:۰۰ ظهر روز بعد
- 💰 ۲۵ هزار تومان

"""

@bot.message_handler(func=lambda m: m.text == get_message("btn.rules"))
@catch_errors(bot)
def show_rules(msg: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("توضیح طرح ها", callback_data="plans"))
    markup.add(InlineKeyboardButton("✅ متوجه شدم", callback_data="ack_rules"))

    bot.send_message(
        chat_id=msg.chat.id,
        text=RULES_TEXT,
        parse_mode="HTML",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda c: c.data == "plans")
@catch_errors(bot)
def plans(call:CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.id,text=PLANS,parse_mode="HTML")


@bot.callback_query_handler(func=lambda c: c.data == "ack_rules")
@catch_errors(bot)
def acknowledge_rules(call):
    bot.answer_callback_query(call.id, "ممنون که قوانین را مطالعه کردید ✅")
    