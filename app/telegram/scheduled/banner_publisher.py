from app.telegram.bot_instance import bot
from config import AVAILABLE_HOURS, MAIN_CHANNEL_ID,ADMINS
from database.session import SessionLocal
from database.models.banner import Banner
from database.repository.reservation_repository import ReservationRepository
from datetime import datetime, time, date
from app.telegram.logger import logger

def publish_approved_reservations():
    logger.info("📅 [Scheduler] Banner publishing job triggered.")
    db = SessionLocal()
    try:
        repo = ReservationRepository(db)
        today = date.today()
        now_time = datetime.now().strftime("%H:%M")

        hours = AVAILABLE_HOURS  # Later: read from DB if available
        for h in hours:
            if h == now_time:
                reservations = repo.get_by_date_time(reserve_date=today, reserve_time=h)
                if reservations:
                    banner: Banner = reservations.banner
                    if not reservations.posted:
                        text = f"📢 رزرو جدید برای امروز:\n{banner.title}"
                        try:
                            bot.send_message(chat_id=MAIN_CHANNEL_ID, text=banner.text)
                        except Exception as e:
                            logger.error(f"❌ Failed to send message to MAIN_CHANNEL_ID={MAIN_CHANNEL_ID}: {e}")
                        for admin in ADMINS:
                            try:
                                logger.info(f"Trying to send message to admin: {admin}")
                                bot.send_message(chat_id=admin, text=text, disable_notification=True)
                            except Exception as e:
                                logger.error(f"❌ Failed to send message to admin {admin}: {e}")
                        reservations.posted = True
                        db.commit()
                break
    
    finally:
        db.close()

def publish_custom_banner(message_text: str, banner_title: str = None):
    logger.info(f"📅 [Scheduler] Custom banner publishing triggered. MAIN_CHANNEL_ID={MAIN_CHANNEL_ID}")
    try:
        bot.send_message(chat_id=MAIN_CHANNEL_ID, text=message_text)
    except Exception as e:
        logger.error(f"❌ Failed to send message to MAIN_CHANNEL_ID={MAIN_CHANNEL_ID}: {e}")
    admin_text = f"📢 رزرو جدید برای امروز:\n{banner_title}" if banner_title else "📢 پیام جدید ارسال شد."
    for admin in ADMINS:
        try:
            logger.info(f"Trying to send message to admin: {admin}")
            bot.send_message(chat_id=admin, text=admin_text, disable_notification=True)
        except Exception as e:
            logger.error(f"❌ Failed to send message to admin {admin}: {e}")