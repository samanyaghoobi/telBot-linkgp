from database.base import Base
from sqlalchemy import Column, Integer, BigInteger, Date, Time, Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        UniqueConstraint("date", "time", name="unique_datetime"),
        UniqueConstraint("date", "link", name="unique_link_per_day"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.userid"), nullable=False)
    banner_id = Column(Integer, ForeignKey("banners.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    price = Column(Integer, default=0)
    posted = Column(Boolean, default=False)
    link = Column(String(255), nullable=False)

    user = relationship("User", back_populates="reservations")
    banner = relationship("Banner", back_populates="reservations")
