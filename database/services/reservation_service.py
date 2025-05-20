from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from datetime import date, time

from database.models.reservation import Reservation
from database.models.user import User
from database.repository.user_repository import UserRepository
from database.repository.reservation_repository import ReservationRepository


def reserve_banner_transaction(
    db: Session,
    user_id: int,
    banner_id: int,
    reserve_date: date,
    reserve_time: time,
    price: int,
    link: str
) -> Optional[Reservation]:
    try:
        user_repo = UserRepository(db)
        reserve_repo = ReservationRepository(db)

        user = user_repo.get_user(user_id)
        if not user or user.balance < price:
            return None

        # Update balance
        user_repo.update_balance(user_id, -price)

        # Create reservation
        reservation = reserve_repo.create_reservation(
            user_id=user_id,
            banner_id=banner_id,
            reserve_date=reserve_date,
            reserve_time=reserve_time,
            link=link,
            price=price
        )

        db.commit()
        return reservation
    except SQLAlchemyError:
        db.rollback()
        return None


def cancel_reservation_transaction(
    db: Session,
    reservation_id: int
) -> bool:
    try:
        reserve_repo = ReservationRepository(db)
        user_repo = UserRepository(db)

        reservation = reserve_repo.get_by_id(reservation_id)
        if not reservation:
            return False

        # Refund balance
        user_repo.update_balance(reservation.user_id, +reservation.price)

        # Delete reservation
        reserve_repo.delete_reservation(reservation_id)

        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        return False
