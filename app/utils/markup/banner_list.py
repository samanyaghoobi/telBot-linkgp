from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.session import SessionLocal
from database.repository.banner_repository import BannerRepository
# 🖼 List user's banners

def build_user_banner_list_markup(user_id: int,callback_data:str="getBanner_")-> InlineKeyboardMarkup:
    db = SessionLocal()
    banner_repo = BannerRepository(db)
    banners = banner_repo.get_active_banners_by_user(user_id)
    
    markup = InlineKeyboardMarkup()
    if not banners:
        markup.add(InlineKeyboardButton("❌ شما هیچ بنر ثبت‌شده فعالی ندارید", callback_data="none"))
        return markup

    for banner in banners:
        markup.add(
            InlineKeyboardButton(
                f"📄 بنر {banner.title}", callback_data=f"{callback_data}{banner.id}"
            )
        )
    return markup