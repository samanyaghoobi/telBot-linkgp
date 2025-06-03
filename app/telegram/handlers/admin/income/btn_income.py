from datetime import datetime, timedelta
import jdatetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from app.telegram.bot_instance import bot
from app.telegram.scheduled.month_income import send_admin_monthly_auto_report
from app.telegram.exception_handler import catch_errors
from app.utils.message import get_message
from database.session import SessionLocal
from database.repository.transaction_repository import TransactionRepository
from database.repository.reservation_repository import ReservationRepository
from config import ADMINS


def get_month_range(target_date: datetime) -> tuple[datetime, datetime]:
    start = target_date.replace(day=1)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


def format_monthly_report(month_title: str, deposit: int, reserve_sum: int, reserve_count: int) -> str:
    avg_price = reserve_sum // reserve_count if reserve_count else 0
    avg_deposit_day = deposit // 30
    avg_count_day = reserve_count / 30 if reserve_count else 0
    
    section1 = f"""📊 گزارش ربات برای ماه {month_title}:

💰 مجموع واریزی: {deposit:,} تومان
💳 مجموع هزینه رزروها: {reserve_sum:,} تومان
📝 تعداد رزروها: {reserve_count}
"""
    
    section2 = f"""
📈 میانگین‌ها در روز:
- 💰 میانگین واریزی: {avg_deposit_day:,} تومان
- 💳 میانگین هزینه رزرو: {avg_price:,} تومان
- 📝 میانگین تعداد رزرو: {avg_count_day:.2f} رزرو

📌 توجه: این گزارش‌ها بر پایه ماه میلادی تهیه شده‌اند.
"""
    return section1 + section2


def format_monthly_comparison(this_month_data, last_month_data, this_month_title):
    def diff(now, past):
        delta = now - past
        symbol = "📈" if delta >= 0 else "📉"
        percent = abs(delta * 100 // past) if past else "∞"
        return f"{symbol} {percent}%"

    t_dep, t_count, t_sum = this_month_data
    l_dep, l_count, l_sum = last_month_data

    msg = f"""📅 مقایسه عملکرد ماهانه:

🟢 این ماه ({this_month_title}):
- 💰 واریزی: {t_dep:,} تومان
- 💳 مجموع رزرو: {t_sum:,} تومان
- 📝 تعداد رزرو: {t_count}

📙 تغییر نسبت به ماه قبل:
- 💰 واریزی: {diff(t_dep, l_dep)}
- 💳 مجموع رزرو: {diff(t_sum, l_sum)}
- 📝 تعداد رزرو: {diff(t_count, l_count)}
"""
    return msg


@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.income"), is_admin=True)
@catch_errors(bot)
def admin_bot_setting_panel(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    today = datetime.today()
    send_admin_monthly_report(msg.chat.id, target_date=today)


def send_admin_monthly_report(chat_id: int, target_date: datetime):
    db = SessionLocal()
    reserve_repo = ReservationRepository(db)
    payment_repo = TransactionRepository(db)

    start_date, end_date = get_month_range(target_date)

    total_deposit = payment_repo.get_total_deposit(start_date.date(), end_date.date())
    reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
    total_reserves = len(reservations)
    total_reserve_price = sum(r.price for r in reservations)

    shamsi = jdatetime.date.fromgregorian(date=start_date.date())
    month_title = f"{shamsi.year}/{shamsi.month}"

    text = format_monthly_report(month_title, total_deposit, total_reserve_price, total_reserves)

    prev_month = (start_date - timedelta(days=1)).replace(day=1)
    next_month = end_date

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⬅️ ماه قبل", callback_data=f"admin_month_stats_{prev_month.date()}"),
        InlineKeyboardButton("➡️ ماه بعد", callback_data=f"admin_month_stats_{next_month.date()}"),
    )
    markup.add(
        InlineKeyboardButton("📊 مقایسه با ماه قبل", callback_data="admin_compare_current_month")
    )

    bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("admin_month_stats_"), is_admin=True)
@catch_errors(bot)
def admin_month_navigation(call: CallbackQuery):
    date_str = call.data.replace("admin_month_stats_", "")
    target_date = datetime.fromisoformat(date_str)

    db = SessionLocal()
    reserve_repo = ReservationRepository(db)
    payment_repo = TransactionRepository(db)

    start_date, end_date = get_month_range(target_date)

    total_deposit = payment_repo.get_total_deposit(start_date.date(), end_date.date())
    reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
    total_reserves = len(reservations)
    total_reserve_price = sum(r.price for r in reservations)

    shamsi = jdatetime.date.fromgregorian(date=start_date.date())
    month_title = f"{shamsi.year}/{shamsi.month}"

    text = format_monthly_report(month_title, total_deposit, total_reserve_price, total_reserves)

    prev_month = (start_date - timedelta(days=1)).replace(day=1)
    next_month = end_date

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("⬅️ ماه قبل", callback_data=f"admin_month_stats_{prev_month.date()}"),
        InlineKeyboardButton("➡️ ماه بعد", callback_data=f"admin_month_stats_{next_month.date()}"),
    )
    markup.add(
        InlineKeyboardButton("📊 مقایسه با ماه قبل", callback_data="admin_compare_current_month")
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda c: c.data == "admin_compare_current_month", is_admin=True)
@catch_errors(bot)
def handle_admin_compare_month(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_admin_monthly_auto_report()

