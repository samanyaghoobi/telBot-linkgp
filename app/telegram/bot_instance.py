from telebot import TeleBot, apihelper
from config import TELEGRAM_API_TOKEN, TELEGRAM_PROXY_URL

bot = TeleBot(TELEGRAM_API_TOKEN)

if TELEGRAM_PROXY_URL:
    apihelper.proxy = {
        'http': TELEGRAM_PROXY_URL,
        'https': TELEGRAM_PROXY_URL
    }
