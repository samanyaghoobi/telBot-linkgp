from sqlalchemy import Column, BigInteger, String, Integer, CheckConstraint
from database.base import Base
from sqlalchemy.orm import relationship, validates

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint('balance >= 0', name='ck_users_balance_non_negative'),
    )

    userid = Column(BigInteger, primary_key=True, index=True)
    balance = Column(Integer, default=0, nullable=False)
    score = Column(Integer, default=0, nullable=False)
    username = Column(String(255), nullable=False)

    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    banners = relationship("Banner", back_populates="user", cascade="all, delete-orphan")

    @validates("balance")
    def _validate_balance(self, key, value):
        if value is None:
            return 0
        if value < 0:
            raise ValueError("Balance cannot be negative")
        return value
