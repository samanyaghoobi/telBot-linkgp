from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.models.reservation import Reservation
from typing import List, Optional
from datetime import date, datetime, time

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, user_id: int, banner_id: int, reserve_date: date, reserve_time: time, link: str, price: int = 0, approved: bool = False) -> Optional[Reservation]:
        reservation = Reservation(
            user_id=user_id,
            banner_id=banner_id,
            date=reserve_date,
            time=reserve_time,
            price=price,
            approved=approved,
            link=link
        )
        try:
            self.db.add(reservation)
            self.db.commit()
            self.db.refresh(reservation)
            return reservation
        except IntegrityError:
            self.db.rollback()
            return None

    def get_by_date_time(self, reserve_date: date, reserve_time: time) -> Optional[Reservation]:
        return self.db.query(Reservation).filter_by(date=reserve_date, time=reserve_time).first()

    def get_reservations_for_date(self, reserve_date: date) -> list[Reservation]:
        return self.db.query(Reservation).filter_by(date=reserve_date).all()

    def get_by_date_and_link(self, reserve_date: date, link: str) -> Optional[Reservation]:
        return self.db.query(Reservation).filter_by(date=reserve_date, link=link).first()

    def get_user_reservations(self, user_id: int) -> List[Reservation]:
        return self.db.query(Reservation).filter_by(user_id=user_id).order_by(Reservation.date, Reservation.time).all()

    def delete_reservation(self, reservation_id: int) -> bool:
        reservation = self.db.query(Reservation).get(reservation_id)
        if reservation:
            self.db.delete(reservation)
            self.db.commit()
            return True
        return False
    
    def get_all_by_user(self, user_id: int) -> List[Reservation]:
        return self.db.query(Reservation).filter_by(user_id=user_id).order_by(Reservation.date, Reservation.time).all()


    def get_upcoming_by_user(self, user_id: int) -> List[Reservation]:
        now = datetime.now()
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.user_id == user_id,
                (Reservation.date > now.date()) |
                ((Reservation.date == now.date()) & (Reservation.time > now.time()))
            )
            .order_by(Reservation.date, Reservation.time)
            .all()
        )

    def get_by_id(self, reservation_id: int) -> Optional[Reservation]:
        return self.db.query(Reservation).get(reservation_id)

    def get_future_reservations_by_banner(self, banner_id: int) -> List[Reservation]:
        now = datetime.now()
        return (
            self.db.query(Reservation)
            .filter(
                Reservation.banner_id == banner_id,
                (Reservation.date > now.date()) |
                ((Reservation.date == now.date()) & (Reservation.time > now.time()))
            )
            .all()
        )
    def get_reservations_from_date(self, from_date: date) -> List[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.date >= from_date)
            .order_by(Reservation.date.asc(), Reservation.time.asc())
            .all()
        )
    def get_reservations_between_dates(self, start: date, end: date) -> list[Reservation]:
        return (
            self.db.query(Reservation)
            .filter(Reservation.date >= start, Reservation.date < end)
            .all()
        )
