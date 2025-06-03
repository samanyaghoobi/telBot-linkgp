from sqlalchemy.orm import Session
from app.telegram.logger import logger
from database.models.bot_setting import BotSetting

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
        except :
            logger.error("error in bot setting")

    def get_all_settings(self) -> list[BotSetting]:
        return self.db.query(BotSetting).all()
