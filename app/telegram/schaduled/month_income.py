from app.telegram.bot_instance import bot
from app.utils.time_tools.covert_time_and_date import date_to_persian, date_to_persian_str
from config import ADMINS
from database.session import SessionLocal
from database.repository.reservation_repository import ReservationRepository
from database.repository.transaction_repository import TransactionRepository
from datetime import datetime, timedelta
import jdatetime
import calendar
from app.utils.logger import logger

def get_month_range(target_date: datetime) -> tuple[datetime, datetime]:
    start = target_date.replace(day=1)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


def format_monthly_report(start_date: datetime, end_date: datetime, deposit: int, reserve_price: int, reserve_count: int) -> str:
    # تاریخ‌های شمسی
    jstart = jdatetime.date.fromgregorian(date=start_date.date())
    jend = jdatetime.date.fromgregorian(date=(end_date - timedelta(days=1)).date())

    # اطلاعات محاسبه شده
    days_count = (end_date - start_date).days
    avg_price_per_reserve = reserve_price // reserve_count if reserve_count else 0
    avg_reserve_per_day = reserve_count / days_count if days_count else 0
    avg_deposit_per_day = deposit / days_count if days_count else 0

    # نام ماه میلادی
    miladi_month = calendar.month_name[start_date.month]
    miladi_range = f"{start_date.strftime('%Y/%m/%d')} تا {(end_date - timedelta(days=1)).strftime('%Y/%m/%d')}"
    shamsi_range = f"{date_to_persian_str(start_date)} تا {date_to_persian_str(end_date)}"

    return f"""
📊 گزارش عملکرد ماه <b>{miladi_month}</b>
📅 بازه زمانی (میلادی): <code>{miladi_range}</code>
📆 معادل شمسی: <code>{shamsi_range}</code>

🟢 آمار کلی:
- 💰 مجموع واریزی: <b>{deposit:,}</b> تومان
- 💳 مجموع هزینه رزروها: <b>{reserve_price:,}</b> تومان
- 📝 تعداد رزرو: <b>{reserve_count}</b>

📘 میانگین‌ها:
- 💵 میانگین قیمت هر رزرو: <b>{avg_price_per_reserve:,}</b> تومان
- 📅 میانگین رزرو روزانه: <b>{avg_reserve_per_day:.2f}</b> رزرو
- 💸 میانگین واریزی روزانه: <b>{avg_deposit_per_day:,.0f}</b> تومان
""".strip()




def format_monthly_comparison(this_data, last_data, this_month_start: datetime) -> str:
    def diff_label(now, past):
        delta = now - past
        symbol = "📈" if delta >= 0 else "📉"
        percent = abs(delta * 100 // past) if past else "∞"
        return f"{symbol} {percent}%"

    t_dep, t_count, t_sum = this_data
    l_dep, l_count, l_sum = last_data

    # Current and previous month names and year
    miladi_month = calendar.month_name[this_month_start.month]
    miladi_year = this_month_start.year

    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    last_month_name = calendar.month_name[last_month_start.month]

    return f"""
📅 <b>مقایسه عملکرد ماهانه</b>
    
🔸 <b>مقایسه بین ماه {miladi_month} و ماه {last_month_name} </b>

🟢 <b>آمار ماه {miladi_month}:</b>
- 💰 مجموع واریزی: <b>{t_dep:,}</b> تومان
- 💳 مجموع هزینه رزرو: <b>{t_sum:,}</b> تومان
- 📝 تعداد رزرو: <b>{t_count}</b>

📙 <b>تغییر نسبت به {last_month_name}:</b>
- 💰 واریزی: {diff_label(t_dep, l_dep)}
- 💳 مجموع رزرو: {diff_label(t_sum, l_sum)}
- 📝 تعداد رزرو: {diff_label(t_count, l_count)}
""".strip()

def send_admin_monthly_auto_report():
    db = SessionLocal()
    reserve_repo = ReservationRepository(db)
    payment_repo = TransactionRepository(db)

    this_month = datetime.today().replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)

    def get_data(start_date):
        end_date = (start_date + timedelta(days=32)).replace(day=1)
        deposit = payment_repo.get_total_deposit(start_date.date(), end_date.date())
        reservations = reserve_repo.get_reservations_between(start_date.date(), end_date.date())
        reserve_price = sum(r.price for r in reservations)
        return deposit, len(reservations), reserve_price, start_date, end_date

    t_dep, t_count, t_sum, t_start, t_end = get_data(this_month)
    l_dep, l_count, l_sum, _, _ = get_data(last_month)

    full_report = format_monthly_report(t_start, t_end, t_dep, t_sum, t_count)
    comparison = format_monthly_comparison((t_dep, t_count, t_sum), (l_dep, l_count, l_sum), t_start)

    msg = f"{full_report}\n\n{comparison}"

    for admin_id in ADMINS:
        bot.send_message(chat_id=admin_id, text=msg, parse_mode="HTML")
        logger.info(f"📊 Monthly income report sent to admin 🧑‍💼 ID: {admin_id}")

