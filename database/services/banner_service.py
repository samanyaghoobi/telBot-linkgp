

from requests import Session

from datetime import datetime
from sqlalchemy.orm import Session
from database.repository.banner_repository import BannerRepository
from database.repository.reservation_repository import ReservationRepository

def soft_delete_banner_transaction(db: Session, banner_id: int, user_id: int) -> bool:
    try:
        banner_repo = BannerRepository(db)
        reserve_repo = ReservationRepository(db)

        banner = banner_repo.get_by_id(banner_id)
        if not banner or banner.user_id != user_id:
            return False

        # استفاده از متد ریپازیتوری برای بررسی رزروهای آینده
        future_reservations = reserve_repo.get_future_reservations_by_banner(banner_id)
        if future_reservations:
            return False  # این بنر در رزروهای آینده استفاده شده

        banner.is_deleted = True
        db.commit()
        return True

    except Exception as e:
        db.rollback()
        raise e

