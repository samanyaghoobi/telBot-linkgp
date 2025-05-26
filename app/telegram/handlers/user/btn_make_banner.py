from telebot.types import Message
from app.telegram.bot_instance import bot
from app.telegram.states.banner_state import BannerStates
from database.session import SessionLocal
from app.utils.messages import get_message
from database.models.banner import Banner
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.user_repository import UserRepository


@bot.message_handler(func=lambda m: m.text == get_message("btn.user.make_banner"))
def start_banner_creation(msg: Message):
    db = SessionLocal()
    user_repo = UserRepository(db)
    setting_repo = BotSettingRepository(db)

    user = user_repo.get_or_create_user(msg.from_user.id, msg.from_user.username)
    user_banners_count = len(user.banners)
    max_allowed = int(setting_repo.bot_setting_get("max_user_banners", "4"))

    if user_banners_count >= max_allowed:
        bot.send_message(msg.chat.id, get_message("error.banner.limit_reached"))
        return

    bot.set_state(msg.from_user.id, BannerStates.waiting_for_title, msg.chat.id)
    bot.send_message(msg.chat.id, get_message("prompt.banner.title"))

@bot.message_handler(state=BannerStates.waiting_for_title)
def get_banner_title(msg: Message):
    bot.set_state(msg.from_user.id, BannerStates.waiting_for_name, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['title'] = msg.text
    bot.send_message(msg.chat.id, get_message("prompt.banner.name"))

@bot.message_handler(state=BannerStates.waiting_for_name)
def get_banner_name(msg: Message):
    bot.set_state(msg.from_user.id, BannerStates.waiting_for_member, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['name'] = msg.text
    bot.send_message(msg.chat.id, get_message("prompt.banner.member"))

@bot.message_handler(state=BannerStates.waiting_for_member)
def get_banner_member(msg: Message):
    if not msg.text.isdigit():
        bot.send_message(msg.chat.id, get_message("error.banner.member"))
        return
    bot.set_state(msg.from_user.id, BannerStates.waiting_for_link, msg.chat.id)
    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        data['member'] = msg.text
    bot.send_message(msg.chat.id, get_message("prompt.banner.link"))

@bot.message_handler(state=BannerStates.waiting_for_link)
def get_banner_link(msg: Message):
    if not (msg.text.startswith("https://t.me/+") or msg.text.startswith("https://t.me/c/")):
        bot.send_message(msg.chat.id, get_message("error.banner.link"))
        return

    with bot.retrieve_data(msg.from_user.id, msg.chat.id) as data:
        title = data['title']
        name = data['name']
        member = data['member']
        link = msg.text

    db = SessionLocal()
    setting_repo = BotSettingRepository(db)
    user_repo = UserRepository(db)

    user = user_repo.get_user(msg.from_user.id)
    banner_format = setting_repo.bot_setting_get("banner_format",
        "Super GP\n\nnaмe: {name}\n\nмeмвer: {member}\n\nlιnĸ: {link}\n\n@LinkGP")
    banner_text = banner_format.format( name=name, member=member, link=link)
    banner_link=link

    new_banner = Banner(title=title,user_id=user.userid, text=banner_text,link=banner_link)
    db.add(new_banner)
    db.commit()

    bot.send_message(msg.chat.id, get_message("success.banner.created"))
    bot.send_message(msg.chat.id, banner_text)
    bot.delete_state(msg.from_user.id, msg.chat.id)
