# main.py
from app.telegram.bot_instance import bot
from app.telegram.schaduled.benner_publisher import publish_approved_reservations
from app.utils.logger import logger
from app.telegram.loader import load_handlers
from app.telegram.handlers.other.startup import startup_message
from app.telegram.filters.is_admin import IsAdminFilter
from database.init import init_db
from apscheduler.schedulers.background import BackgroundScheduler
from app.telegram.handlers.admin.income.btn_income import send_admin_monthly_auto_report

if __name__ == "__main__":
    init_db()
    logger.info("📦 Database initialized.")

    bot.add_custom_filter(IsAdminFilter())
    logger.info("🔒 Custom filters registered.")

    load_handlers(bot)
    logger.info("📁 Handlers loaded.")

    startup_message(bot)
    logger.info("🚀 Startup message sent.")

    scheduler = BackgroundScheduler()
    scheduler.add_job(send_admin_monthly_auto_report, "cron", day=1, hour=8) # every month at 8 AM at first day 
    logger.info("📅 Monthly report scheduler started.")
    scheduler.add_job(publish_approved_reservations, "interval", seconds=60)
    logger.info("publish branche is started  scheduler started.")
    scheduler.start()

    bot.infinity_polling(skip_pending=True)
    logger.info("🤖 Bot is running...")
