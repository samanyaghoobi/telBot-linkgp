
from app.telegram.bot_instance import bot
from app.telegram.filters.is_admin import IsAdminFilter
from app.telegram.loader import load_handlers
from app.utils.logger import logger
from database.base import SessionLocal
from database.init import init_db


# Register custom filters
bot.add_custom_filter(IsAdminFilter())

# Dynamically load all handlers

if __name__ == "__main__":
    print("🤖 Bot is running...")
    init_db()


    logger.info("🤖 Bot is starting...")

    if bot :
        load_handlers(bot)
    bot.infinity_polling()
    # thread = Thread(target=bot.infinity_polling, daemon=True)
    # thread.start()