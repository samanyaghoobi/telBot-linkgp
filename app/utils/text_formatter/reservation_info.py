from datetime import date, time
from app.utils.time_tools.covert_time_and_date import date_to_persian
from database.session import SessionLocal
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository

# Format reservation details for user/admin messages
def format_reservation_message(reserve_date: date, reserve_time: time, price: int = 0, banner_title: str = None, link: str = None, extra: str = None) -> str:
    shamsi_date = date_to_persian(reserve_date)
    time_str = reserve_time.strftime("%H:%M")
    parts = [
        f"📅 تاریخ:\n {shamsi_date}",
        f"⏰ ساعت: {time_str}",
        f"💰 مبلغ: {price:,} تومان"
    ]
    if banner_title:
        parts.append(f"🏷 بنر: {banner_title}")
    if link:
        parts.append(f"🔗 لینک: {link}")
    if extra:
        parts.append(extra)

    return "\n".join(parts)

# Format reservation details from DB by reservation ID
def format_reservation_by_id(reservation_id: int) -> str:
    db = SessionLocal()
    repo = ReservationRepository(db)
    banner_repo = BannerRepository(db)

    reservation = repo.get_by_id(reservation_id)
    if not reservation:
        return "❌ رزرو یافت نشد."

    banner = banner_repo.get_by_id(reservation.banner_id)
    banner_title = banner.title if banner else "بنر حذف شده"

    return format_reservation_message(
        reserve_date=reservation.date,
        reserve_time=reservation.time,
        price=reservation.price,
        banner_title=banner_title,
        link=banner.link
    )
