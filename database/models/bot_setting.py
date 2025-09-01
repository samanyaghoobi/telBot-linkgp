from database.base import Base
from sqlalchemy import Column, String, Text

class BotSetting(Base):
    __tablename__ = "setting"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
