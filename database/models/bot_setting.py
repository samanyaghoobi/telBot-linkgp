from sqlalchemy import Column, String, Text
from database.base import Base

class BotSetting(Base):
    __tablename__ = "setting"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
