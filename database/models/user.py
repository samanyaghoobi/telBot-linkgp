from sqlalchemy import Column, BigInteger, String, Integer
from database.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    userid = Column(BigInteger, primary_key=True, index=True)
    balance = Column(Integer, default=0)
    score = Column(Integer, default=0)
    username = Column(String(255), nullable=False)

    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    banners = relationship("Banner", back_populates="user", cascade="all, delete-orphan")
