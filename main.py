# main.py
from app.telegram.bot_instance import bot
from app.telegram.loader import load_handlers
from app.telegram.scheduled.banner_publisher import publish_approved_reservations
from app.telegram.logger import logger
from app.telegram.handlers.other.startup import startup_message
from app.telegram.filters.filters import IsAdminFilter, is_button, NoStateFilter
from app.telegram.scheduled.sql_backup import send_latest_backup_to_channel
from app.utils.messages.delete_message import delete_scheduled_messages
from database.init import init_db
from apscheduler.schedulers.background import BackgroundScheduler
from app.telegram.handlers.admin.income.btn_income import send_admin_monthly_auto_report
if __name__ == "__main__":
    init_db()
    logger.info("📦 Database initialized.")

    bot.add_custom_filter(IsAdminFilter())
    bot.add_custom_filter(NoStateFilter())
    bot.add_custom_filter(is_button())
    logger.info("🔒 Custom filters registered.")

    load_handlers(bot)
    logger.info("📁 Handlers loaded.")

    startup_message(bot)
    logger.info("🚀 Startup message sent.")

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_admin_monthly_auto_report, "cron", day=1, hour=8) # every month at 8 AM at first day 
    logger.info("📅 Monthly report scheduler started.")

    scheduler.add_job(delete_scheduled_messages, "interval", seconds=10)
    logger.info("🧹 Scheduled message deletion job registered.")

    scheduler.add_job(publish_approved_reservations, "interval", seconds=60)
    logger.info("publish branch is started  scheduler started.")

    scheduler.add_job(send_latest_backup_to_channel, "cron", hour=2, minute=43)


    scheduler.start()

    bot.infinity_polling(skip_pending=True)
    logger.info("🤖 Bot is running...")
