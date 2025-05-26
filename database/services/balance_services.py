from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.telegram.bot_instance import bot
from app.telegram.handlers.other.exception_handler import catch_errors
from database.repository.user_repository import UserRepository


def convert_score_to_balance_transaction(
    db: Session,
    user_id: int,
    rate: int
) -> tuple[bool, int, int]:
    """
    تلاش برای تبدیل score به balance.
    برمی‌گرداند:
        - موفقیت یا شکست
        - مقدار امتیاز مصرف‌شده
        - مقدار تومان افزوده‌شده
    """
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user(user_id)

        if not user or user.score < rate:
            return False, 0, 0

        toman = user.score // rate
        used_score = toman * rate

        if toman <= 0:
            return False, 0, 0

        user_repo.update_balance(user_id, +toman)
        user_repo.update_score(user_id, -used_score)

        db.commit()
        return True, used_score, toman

    except SQLAlchemyError:
        db.rollback()
        return False, 0, 0

@catch_errors(bot)
def charge_user_transaction(db, user_id: int, amount: int) -> bool:
    from database.repository.user_repository import UserRepository
    from database.models.transaction import Transaction

    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user(user_id)
        if not user:
            return False

        new_balance = user.balance + amount
        user_repo.update_balance(user_id, amount)
        print("-----------------")
        db.add(Transaction(
            user_id=user_id,
            amount=amount,
            type="charge",
            balance_after=new_balance
        ))

        db.commit()
        print("-----------------")
        return True
    except Exception as e:
        print (e)
        db.rollback()
        return False
