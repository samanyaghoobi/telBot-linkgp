from telebot import TeleBot, apihelper,custom_filters
from config import TELEGRAM_API_TOKEN, TELEGRAM_PROXY_URL
import coloredlogs

coloredlogs.install(level="INFO", fmt="%(asctime)s [%(levelname)s] %(message)s")

bot = TeleBot(TELEGRAM_API_TOKEN,colorful_logs=True,skip_pending=True,disable_web_page_preview=True)

bot.add_custom_filter(custom_filters.StateFilter(bot))

if TELEGRAM_PROXY_URL:
    apihelper.proxy = {
        'http': TELEGRAM_PROXY_URL,
        'https': TELEGRAM_PROXY_URL
    }
