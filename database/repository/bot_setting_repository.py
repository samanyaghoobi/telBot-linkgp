from database.models.bot_setting import BotSetting
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

class BotSettingRepository:
    def __init__(self, db: Session):
        self.db = db

    def bot_setting_get(self, key: str, default: str = "") -> str:
        setting = self.db.query(BotSetting).filter_by(key=key).first()
        return setting.value if setting else default

    def bot_setting_set(self, key: str, value: str):
        try:
            setting = self.db.query(BotSetting).filter_by(key=key).first()
            if setting:
                setting.value = value
            else:
                setting = BotSetting(key=key, value=value)
                self.db.add(setting)
            self.db.commit()
        except Exception as e:
            logger.error(f"Error in bot setting: {e}")
            self.db.rollback()

    def get_all_settings(self) -> list:
        return self.db.query(BotSetting).all()

    def bot_setting_add(self, key: str, value: str):
        try:
            # Check if the setting already exists
            setting = self.db.query(BotSetting).filter_by(key=key).first()
            if not setting:
                # Add new setting if not exists
                setting = BotSetting(key=key, value=value)
                self.db.add(setting)
                self.db.commit()
                logger.info(f"Setting added: {key} = {value}")
            else:
                logger.info(f"Setting with key '{key}' already exists.")
        except Exception as e:
            logger.error(f"Error adding bot setting: {e}")
            self.db.rollback()

    def bot_setting_delete(self, key: str):
        try:
            setting = self.db.query(BotSetting).filter_by(key=key).first()
            if setting:
                self.db.delete(setting)
                self.db.commit()
                logger.info(f"Setting deleted: {key}")
            else:
                logger.warning(f"Setting not found for deletion: {key}")
        except Exception as e:
            logger.error(f"Error deleting bot setting: {e}")
            self.db.rollback()
