from app.telegram.bot_instance import bot
from config import AVAILABLE_HOURS, MAIN_CHANNEL_ID
from database.session import SessionLocal
from database.models.banner import Banner
from database.repository.reservation_repository import ReservationRepository
from datetime import datetime, time, date
import logging

def publish_approved_reservations():
    db = SessionLocal()
    repo = ReservationRepository(db)
    today = date.today()
    now_time = datetime.now().strftime("%H:%M")

    hours = AVAILABLE_HOURS  # Later: read from DB if available
    for h in hours:
        if h == now_time:
            reservations = repo.get_approved_not_posted(today, time.fromisoformat(h))
            for r in reservations:
                banner :Banner = r.banner
                # text = f"📢 رزرو جدید برای امروز:\n{banner.title}"
                # bot.send_message(chat_id=POST_CHANNEL_ID, text=text)
                bot.send_message(chat_id=MAIN_CHANNEL_ID, text=banner.text)
                r.posted = True
                db.commit()
            break