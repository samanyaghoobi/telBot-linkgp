from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.utils.message import get_message
from database.session import SessionLocal
from database.repository.banner_repository import BannerRepository
# 🖼 List user's banners

def build_user_banner_list_markup(user_id: int,callback_data:str="getBanner_")-> InlineKeyboardMarkup:
    db = SessionLocal()
    banner_repo = BannerRepository(db)
    banners = banner_repo.get_active_banners_by_user(user_id)
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text=get_message("btn.user.make_banner"),callback_data=get_message("btn.user.make_banner")))
    if not banners:
        markup.add(InlineKeyboardButton("❌ شما هیچ بنر ثبت‌شده فعالی ندارید", callback_data="none"))
        return markup

    for banner in banners:
        markup.add(
            InlineKeyboardButton(
                f"📄 بنر :{banner.title}", callback_data=f"{callback_data}{banner.id}"
            )
        )
    return markup