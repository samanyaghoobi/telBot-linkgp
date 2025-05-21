from app.telegram.bot_instance import bot
from app.telegram.filters.is_admin import IsAdminFilter
from app.telegram.handlers.admin.income.btn_income import send_admin_monthly_auto_report
from app.telegram.handlers.other.startup import startup_message
from app.telegram.loader import load_handlers
from app.utils.logger import logger
from database.init import init_db
from apscheduler.schedulers.background import BackgroundScheduler

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
    scheduler.add_job(send_admin_monthly_auto_report, "cron", day=1, hour=8, minute=0)
    scheduler.start()
    logger.info("📅 Monthly report scheduler started.")

    logger.info("🤖 Bot is running...")
    bot.infinity_polling(skip_pending=True)
