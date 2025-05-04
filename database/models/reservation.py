from sqlalchemy import BigInteger, Column, Integer, ForeignKey, Date, Time, Boolean, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database.base import Base
from datetime import datetime

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.userid"))
    banner_id = Column(Integer, ForeignKey("banners.id"))

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    price = Column(Integer, default=0)
    approved = Column(Boolean, default=False)
    status = Column(String(50), default="pending")  # sent / canceled / failed
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="reservations")
    banner = relationship("Banner", backref="reservations")

    __table_args__ = (
        UniqueConstraint("date", "time", name="unique_slot_per_day"),
    )
