from app.telegram.bot_instance import bot
from config import AVAILABLE_HOURS, MAIN_CHANNEL_ID
from database.session import SessionLocal
from database.models.banner import Banner
from database.repository.reservation_repository import ReservationRepository
from datetime import datetime, time, date
from app.telegram.logger import logger

def publish_approved_reservations():
    logger.info("📅 [Scheduler] Banner publishing job triggered.")
    db = SessionLocal()
    repo = ReservationRepository(db)
    today = date.today()
    now_time = datetime.now().strftime("%H:%M")

    hours = AVAILABLE_HOURS  # Later: read from DB if available
    for h in hours:
        if h == now_time:
            reservations = repo.get_by_date_time(reserve_date=today,reserve_time=h)
            if reservations:
                banner :Banner = reservations.banner
                if not reservations.posted:
                    text = f"📢 رزرو جدید برای امروز:\n{banner.title}"
                    # notify_admin # todo
                    bot.send_message(chat_id=MAIN_CHANNEL_ID, text=banner.text)
                    reservations.posted = True
                    db.commit()
            break