from sqlalchemy import BigInteger, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.userid"))
    title = Column(String(255))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="banners")
