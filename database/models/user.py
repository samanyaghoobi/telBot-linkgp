from sqlalchemy import Column, BigInteger, Integer, String, DateTime
from database.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    userid = Column(BigInteger, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    balance = Column(Integer, default=0)
    score = Column(Integer, default=0)
