from datetime import date, datetime, timedelta
import jdatetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery
from app.telegram.bot_instance import bot
from app.utils.message import get_message
from database.session import SessionLocal
from database.models.banner import Banner
from database.models.reservation import Reservation
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository
from database.repository.user_repository import UserRepository

@bot.message_handler(func=lambda m: m.text == get_message("btn.user.my_reservations"))
def my_reservation(msg: Message):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🕓 فقط رزروهای آینده", callback_data="show_future_reservations"),
        InlineKeyboardButton("🔁 نمایش همه رزروها", callback_data="show_all_reservations")
    )
    bot.send_message(
        msg.chat.id,
        "📋 لطفاً انتخاب کن کدوم نوع رزروها رو می‌خوای ببینی:",
        reply_markup=markup
    )
    

@bot.callback_query_handler(func=lambda c: c.data.startswith("show_future_reservations") or c.data.startswith("show_all_reservations"))
def show_reservations(call: CallbackQuery):
    bot.delete_state(call.message.chat.id, call.message.chat.id)
    db = SessionLocal()
    try:
        repo = ReservationRepository(db)
        banner_repo = BannerRepository(db)

        user_id = call.from_user.id
        today = date.today()
        now = datetime.now()

        # Parse callback data
        raw_data = call.data.split(":")
        mode = raw_data[0]  # show_all_reservations OR show_future_reservations
        base_date = today
        if len(raw_data) > 1:
            base_date = date.fromisoformat(raw_data[1])

        # Adjust to start week from Saturday
        weekday = (base_date.weekday() + 2) % 7  # Saturday=0
        start_of_week = base_date - timedelta(days=weekday)
        end_of_week = start_of_week + timedelta(days=6)

        # Load reservations
        if mode == "show_future_reservations":
            all_reservations = repo.get_upcoming_by_user(user_id)
            title = "🕓 رزروهای آینده شما:"
        else:
            all_reservations = repo.get_all_by_user(user_id)
            title = "📋 تمام رزروهای شما:"

        # Filter current week reservations
        reservations = [
            r for r in all_reservations
            if start_of_week <= r.date <= end_of_week
        ]

        markup = InlineKeyboardMarkup(row_width=1)
        if not reservations:
            markup.add(InlineKeyboardButton("❌ هیچ رزروی برای این هفته یافت نشد", callback_data="none"))
        else:
            for reserve in reservations:
                is_future = (
                    reserve.date > today or
                    (reserve.date == today and reserve.time > now.time())
                )

                # Convert date to Jalali
                day_shamsi = jdatetime.date.fromgregorian(date=reserve.date)
                show_year = day_shamsi.year != jdatetime.date.today().year
                jdate_str = f"{day_shamsi.month}/{day_shamsi.day}"
                if show_year:
                    jdate_str = f"{day_shamsi.year}/{jdate_str}"

                # Get banner title
                banner = banner_repo.get_by_id(reserve.banner_id)
                banner_title = banner.title if banner else "بنر نامشخص"

                icon = "🟢" if is_future else "⚪️"
                button_text = f"{icon} {banner_title} | {jdate_str} - {reserve.time.strftime('%H:%M')}"
                markup.add(
                    InlineKeyboardButton(button_text, callback_data=f"show_reservation_{reserve.id}:{mode}")
                )

        # Pagination Buttons
        has_prev = any(r.date < start_of_week for r in all_reservations)
        has_next = any(r.date > end_of_week for r in all_reservations)

        nav_buttons = []
        if has_prev:
            prev_date = start_of_week - timedelta(days=7)
            nav_buttons.append(
                InlineKeyboardButton("⬅️ هفته قبل", callback_data=f"{mode}:{prev_date.isoformat()}")
            )
        if has_next:
            next_date = start_of_week + timedelta(days=7)
            nav_buttons.append(
                InlineKeyboardButton("➡️ هفته بعد", callback_data=f"{mode}:{next_date.isoformat()}")
            )
        if nav_buttons:
            markup.add(*nav_buttons)

        week_range_jalali = f"{jdatetime.date.fromgregorian(date=start_of_week).strftime('%Y/%m/%d')} تا {jdatetime.date.fromgregorian(date=end_of_week).strftime('%Y/%m/%d')}"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f"{title}\n🗓 هفته: {week_range_jalali}",
            reply_markup=markup
        )
    finally:
        db.close()
