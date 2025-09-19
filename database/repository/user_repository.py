from typing import Optional, List
from sqlalchemy.orm import Session
from database.models.user import User
from sqlalchemy.exc import SQLAlchemyError
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_user(self, userid: int, username: Optional[str]) -> User:
        user = self.db.query(User).filter_by(userid=userid).first()
        if not user:
            # Ensure username is never NULL to satisfy DB constraint
            safe_username = (username or "").strip()
            user = User(userid=userid, username=safe_username)
            self.db.add(user)
            self.db.commit()
        return user

    
    def update_balance(self, userid: int, amount: int):
        try:
            user = self.db.query(User).filter_by(userid=userid).first()
            if user:
                new_balance = (user.balance or 0) + amount
                if new_balance < 0:
                    # Prevent negative balances
                    raise ValueError("Insufficient balance: result would be negative")
                user.balance = new_balance

                self.db.flush()  
                
                self.db.commit()
                
                return True
            else:
                return None

        except SQLAlchemyError as e:
            self.db.rollback()
            return None  


    def get_user(self, userid: int) -> Optional[User]:
        return self.db.query(User).filter_by(userid=userid).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()



    def update_score(self, user_id: int, amount: int):
        try:
            user = self.get_user(user_id)
            
            if user:
                
                user.score += amount
                
                self.db.flush()  
                self.db.commit()
                
            else:
                return None 

        except SQLAlchemyError as e:
            self.db.rollback()
            return None 

        return user 
