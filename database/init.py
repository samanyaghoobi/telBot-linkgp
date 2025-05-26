# database/init.py
from database.base import Base
from database.session import engine

# 👇 تمام مدل‌ها اینجا ایمپورت بشن
from database.models.user import User
from database.models.banner import Banner
from database.models.reservation import Reservation
from database.models.transaction import Transaction
from database.models.bot_setting import BotSetting

def init_db():
    Base.metadata.create_all(bind=engine)