from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String, DateTime
from database.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.userid"))
    amount = Column(Integer, nullable=False)
    type = Column(String(50), default="charge")  # charge / refund / bonus / use
    balance_after = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="transaction")
