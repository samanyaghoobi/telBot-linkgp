from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.models.banner import Banner
# 🖼 List user's banners
def build_user_banner_list_markup(banners: list[Banner]):
    markup = InlineKeyboardMarkup()
    for banner in banners:
        print(banner)
        markup.add(
            InlineKeyboardButton(f"📄 بنر {banner.title}", callback_data=f"getBanner_{banner.id}")
        )
    return markup
