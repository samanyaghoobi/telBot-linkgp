# database/init.py
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from database.base import Base
from database.session import engine

from database.models.user import User
from database.models.banner import Banner
from database.models.reservation import Reservation
from database.models.transaction import Transaction
from database.models.bot_setting import BotSetting


logger = logging.getLogger(__name__)


def is_database_available() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as exc:
        logger.error("Database connectivity check failed: %s", exc)
        return False


def init_db():
    Base.metadata.create_all(bind=engine)
