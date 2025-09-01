from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from typing import Optional
from datetime import date, datetime, time, timedelta
from app.telegram.logger import logger
from app.utils.time_tools.covert_time_and_date import date_to_persian
from database.models.reservation import Reservation
from database.models.user import User
from database.repository.banner_repository import BannerRepository
from database.repository.bot_setting_repository import BotSettingRepository
from database.repository.user_repository import UserRepository
from database.repository.reservation_repository import ReservationRepository

from typing import Optional
from datetime import date, time



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

        # validate user
        user = user_repo.get_user(user_id)
        if not user:
            logger.error(f"Reservation failed: user not found (user_id={user_id})")
            return None
        if user.balance < price:
            logger.error(f"Reservation failed: insufficient balance (user_id={user_id}, balance={user.balance}, price={price})")
            return None

        # update balance
        try:
            user_repo.update_balance(user_id, -price)
        except Exception as e:
            db.rollback()
            logger.error(f"Reservation failed: error updating balance (user_id={user_id}, error={e})")
            return None

        # create reservation
        try:
            reservation = reserve_repo.create_reservation(
                user_id=user_id,
                banner_id=banner_id,
                reserve_date=reserve_date,
                reserve_time=reserve_time,
                link=link,
                price=price
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Reservation failed: error creating reservation (user_id={user_id}, banner_id={banner_id}, date={reserve_date}, time={reserve_time}, error={e})")
            return None

        db.commit()
        return reservation

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Reservation failed: SQLAlchemyError (user_id={user_id}, banner_id={banner_id}, date={reserve_date}, time={reserve_time}, error={e})")
        return None

    except Exception as e:
        db.rollback()
        logger.error(f"Reservation failed: unexpected error (user_id={user_id}, banner_id={banner_id}, date={reserve_date}, time={reserve_time}, error={e})")
        return None

# def reserve_banner_transaction(
#     db: Session,
#     user_id: int,
#     banner_id: int,
#     reserve_date: date,
#     reserve_time: time,
#     price: int,
#     link: str
# ) -> Optional[Reservation]:
#     try:
#         user_repo = UserRepository(db)
#         reserve_repo = ReservationRepository(db)

#         user = user_repo.get_user(user_id)
#         if not user or user.balance < price:
#             return None

#         # Update balance
#         user_repo.update_balance(user_id, -price)

#         # Create reservation
#         reservation = reserve_repo.create_reservation(
#             user_id=user_id,
#             banner_id=banner_id,
#             reserve_date=reserve_date,
#             reserve_time=reserve_time,
#             link=link,
#             price=price
#         )

#         db.commit()

#         return reservation
#     except SQLAlchemyError as e:
#         db.rollback()
#         return None


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

def reserve_custom_range_transaction(db, user_id: int, banner_id: int, from_date: date, to_date: date, hour: str) -> tuple[bool, str]:
    try:
        user_repo = UserRepository(db)
        res_repo = ReservationRepository(db)
        banner_repo = BannerRepository(db)
        setting_repo = BotSettingRepository(db)

        user = user_repo.get_user(user_id)
        banner = banner_repo.get_by_id(banner_id)

        if not user or not banner:
            return False, "❌ بنر یا کاربر یافت نشد."

        rate = int(setting_repo.bot_setting_get("price_per_hour", "50"))
        total_days = (to_date - from_date).days + 1
        max_total_price = rate * total_days

        if user.balance < rate:
            return False, f"❌ موجودی شما برای این رزرو کافی نیست. حداقل موجودی مورد نیاز: {rate:,} تومان"

        reserved = []
        failed = []

        current_date = from_date
        while current_date <= to_date:
            try:
                reservation = res_repo.create_reservation(
                    user_id=user_id,
                    banner_id=banner_id,
                    reserve_date=current_date,
                    reserve_time=datetime.strptime(hour, "%H:%M").time(),
                    link=banner.link,
                    price=rate
                )
                current_shamsi=date_to_persian(current_date)
                if reservation:
                    user_repo.update_balance(user_id, -rate)
                    reserved.append(f"{current_shamsi} ساعت {hour}")
                else:
                    failed.append(f"{current_shamsi} ساعت {hour} ❌ قبلاً رزرو شده")
            except IntegrityError:
                db.rollback()
                failed.append(f"{current_shamsi} ساعت {hour} ❌ خطای تکراری")
            except Exception as e:
                db.rollback()
                failed.append(f"{current_shamsi} ساعت {hour} ❌ {str(e)}")

            current_date += timedelta(days=1)

        if reserved:
            db.commit()
        else:
            return False, "❌ هیچ رزروی ثبت نشد."

        success_text = "✅ رزروهای موفق:\n" + "\n".join(reserved) if reserved else ""
        failed_text = "\n\n⚠️ رزروهای ناموفق:\n" + "\n".join(failed) if failed else ""

        return True, f"{success_text}{failed_text}"

    except SQLAlchemyError as e:
        db.rollback()
        return False, f"❌ خطای پایگاه داده: {str(e)}"

    except Exception as e:
        db.rollback()
        return False, f"❌ خطای نامشخص: {str(e)}"
