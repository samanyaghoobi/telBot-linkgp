
from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.telegram.bot_instance import bot
from app.telegram.exception_handler import catch_errors
from database.session import SessionLocal
from database.repository.user_repository import UserRepository
from database.repository.bot_setting_repository import BotSettingRepository
from database.services.balance_services import convert_score_to_balance_transaction

@bot.callback_query_handler(func=lambda c: c.data == "convert_points")
@catch_errors(bot)
def handle_point_conversion(call: CallbackQuery):
    db = SessionLocal()
    user_repo = UserRepository(db)
    setting_repo = BotSettingRepository(db)

    user = user_repo.get_user(call.from_user.id)
    if not user:
        bot.answer_callback_query(call.id, "کاربر یافت نشد.", show_alert=True)
        return

    # نرخ تبدیل از تنظیمات یا دیفالت
    rate_str = setting_repo.bot_setting_get("point_to_toman", "10")
    try:
        rate = int(rate_str)
    except ValueError:
        rate = 10

    if user.score < rate:
        bot.answer_callback_query(call.id, "❌ حداقل امتیاز برای تبدیل کافی نیست.", show_alert=True)
        return

    # محاسبه مبلغ قابل تبدیل
    toman = user.score // rate
    formatted_toman = f"{toman:,}"

    message = (
        f"📌 شما {user.score} امتیاز دارید.\n"
        f"🔄 نرخ تبدیل: هر {rate} امتیاز = ۱ هزارتومان\n"
        f"💰 مبلغ قابل تبدیل: {formatted_toman}   هزارتومان\n\n"
        f"آیا مایلید امتیازهای شما به موجودی تبدیل شود؟"
    )

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ تایید تبدیل", callback_data="confirm_convert_score"),
        InlineKeyboardButton("❌ لغو", callback_data="cancel")
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=message,
        reply_markup=markup
    )



@bot.callback_query_handler(func=lambda c: c.data == "confirm_convert_score")
@catch_errors(bot)
def confirm_point_conversion(call: CallbackQuery):
    db = SessionLocal()
    user_repo = UserRepository(db)
    setting_repo = BotSettingRepository(db)

    user = user_repo.get_user(call.from_user.id)
    if not user:
        bot.answer_callback_query(call.id, "کاربر یافت نشد.", show_alert=True)
        return

    # نرخ تبدیل
    try:
        rate = int(setting_repo.bot_setting_get("point_to_toman", "10"))
    except ValueError:
        rate = 10

    # تبدیل امتیاز به تومان با تراکنش
    success, used_score, toman = convert_score_to_balance_transaction(
        db=db,
        user_id=user.userid,
        rate=rate
    )

    if not success:
        bot.answer_callback_query(call.id, "❌ امتیاز کافی برای تبدیل وجود ندارد.", show_alert=True)
        return

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ {used_score:,} امتیاز شما به {toman:,} تومان تبدیل شد و به موجودی شما افزوده شد."
    )

