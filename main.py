
from app.telegram.bot_instance import bot
from app.telegram.filters.is_admin import IsAdminFilter
from app.telegram.handlers.other.startup import startup_message
from app.telegram.loader import load_handlers
from app.utils.logger import logger
from database.init import init_db

# Register custom filters
bot.add_custom_filter(IsAdminFilter())

# Dynamically load all handlers

if __name__ == "__main__":
    # print("🤖 Bot is running...")
    init_db()


    logger.info("🤖 Bot is starting...!")

    if bot :
        load_handlers(bot)
    startup_message(bot)
    bot.infinity_polling(skip_pending=True)
    # thread = Thread(target=bot.infinity_polling, daemon=True)
    # thread.start()