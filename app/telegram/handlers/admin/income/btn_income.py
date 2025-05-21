from app.telegram.handlers.other.exception_handler import catch_errors
from app.utils.messages import get_message
from app.telegram.bot_instance import bot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMINS
from database.base import SessionLocal
from database.repository.reservation_repository import ReservationRepository
from datetime import datetime, timedelta
import jdatetime
from apscheduler.schedulers.background import BackgroundScheduler


def get_month_range(target_date: datetime) -> tuple[datetime, datetime]:
    start = target_date.replace(day=1)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


@bot.message_handler(func=lambda m: m.text == get_message("btn.admin.income"), is_admin=True)
@catch_errors(bot)
def admin_bot_setting_panel(msg: Message):
    today = datetime.today()
    send_admin_monthly_report(msg.chat.id, target_date=today)


def send_admin_monthly_report(chat_id: int, target_date: datetime):
    db = SessionLocal()
    reserve_repo = ReservationRepository(db)
    # payment_repo = TransactionRepository(db)

    start_date, end_date = get_month_range(target_date)

    # total_deposit = payment_repo.get_total_deposit(start_date.date(), end_date.date())
    reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
    total_reserves = len(reservations)
    total_reserve_price = sum(r.price for r in reservations)

    shamsi = jdatetime.date.fromgregorian(date=start_date.date())
    month_title = f"{shamsi.year}/{shamsi.month}"

# 💰 مجموع واریزی: {total_deposit:,} تومان
    text = f"""📊 گزارش ربات برای ماه {month_title}:


📝 تعداد رزرو: {total_reserves}
💳 مجموع هزینه رزروها: {total_reserve_price:,} تومان
"""

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
    start_date, end_date = get_month_range(target_date)
    reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
    total_reserves = len(reservations)
    total_reserve_price = sum(r.price for r in reservations)
    shamsi = jdatetime.date.fromgregorian(date=start_date.date())
    month_title = f"{shamsi.year}/{shamsi.month}"

    text = f"""📊 گزارش ربات برای ماه {month_title}:

📝 تعداد رزرو: {total_reserves}
💳 مجموع هزینه رزروها: {total_reserve_price:,} تومان
"""

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
def handle_admin_compare_month(call: CallbackQuery):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    send_admin_monthly_auto_report()


def send_admin_monthly_auto_report():
    db = SessionLocal()
    reserve_repo = ReservationRepository(db)
    # payment_repo = TransactionRepository(db)0

    this_month = datetime.today().replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)

    def get_data_range(start_date):
        end_date = (start_date + timedelta(days=32)).replace(day=1)
        # total_deposit = payment_repo.get_total_deposit(start_date.date(), end_date.date())
        reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
        total_reserve_price = sum(r.price for r in reservations)
        return  len(reservations), total_reserve_price
        # return total_deposit, len(reservations), total_reserve_price

    t_count, t_sum = get_data_range(this_month)
    l_count, l_sum = get_data_range(last_month)
     
    # t_dep, t_count, t_sum = get_data_range(this_month)
    # l_dep, l_count, l_sum = get_data_range(last_month)

    def diff(now, past):
        delta = now - past
        symbol = "📈" if delta >= 0 else "📉"
        percent = abs(delta * 100 // past) if past else "∞"
        return f"{symbol} {percent}%"

# - 💰 واریزی: {t_dep:,}
# - 💰 واریزی: {diff(t_dep, l_dep)}

    msg = f"""📅 مقایسه عملکرد ماهانه:

🟢 این ماه ({jdatetime.date.fromgregorian(date=this_month.date())}):
- 📝 رزرو: {t_count}
- 💳 مجموع رزرو: {t_sum:,}

📙 تغییر نسبت به ماه قبل:
- 📝 رزرو: {diff(t_count, l_count)}
- 💳 مجموع رزرو: {diff(t_sum, l_sum)}
"""

    for admin_id in ADMINS:
        bot.send_message(chat_id=admin_id, text=msg)


