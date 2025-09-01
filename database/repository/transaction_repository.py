from sqlalchemy.orm import Session
from database.models.transaction import Transaction
from datetime import date


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_deposit(self, from_date: date, to_date: date) -> int:
        result = self.db.query(Transaction).filter(
            Transaction.type == "charge",
            Transaction.created_at >= from_date,
            Transaction.created_at < to_date
        ).all()
        return sum(tx.amount for tx in result)
