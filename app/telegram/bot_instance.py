from telebot import TeleBot, apihelper,custom_filters
from app.telegram.handlers.exception_handler import MyExceptionHandler
from config import TELEGRAM_API_TOKEN, TELEGRAM_PROXY_URL
import logging
import coloredlogs

coloredlogs.install(level="INFO", fmt="%(asctime)s [%(levelname)s] %(message)s")

bot = TeleBot(TELEGRAM_API_TOKEN, exception_handler=MyExceptionHandler(),colorful_logs=True)

bot.add_custom_filter(custom_filters.StateFilter(bot))

if TELEGRAM_PROXY_URL:
    apihelper.proxy = {
        'http': TELEGRAM_PROXY_URL,
        'https': TELEGRAM_PROXY_URL
    }
