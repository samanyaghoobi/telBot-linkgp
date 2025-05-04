from typing import Optional,List
from sqlalchemy.orm import Session
from database.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user(self, userid: int, username: str) -> User:
        user = self.db.query(User).filter_by(userid=userid).first()
        if not user:
            user = User(userid=userid, username=username)
            self.db.add(user)
            self.db.commit()
        return user

    def update_balance(self, userid: int, amount: int):
        user = self.db.query(User).filter_by(userid=userid).first()
        if user:
            user.balance += amount
            self.db.commit()

    def get_user(self, userid: int) -> Optional[User]:
        return self.db.query(User).filter_by(userid=userid).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

