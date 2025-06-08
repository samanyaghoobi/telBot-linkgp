from database.repository.user_repository import UserRepository

def create_user_if_not_exists(db, user_id: int, username: str) -> bool:
    try:
        user_repo = UserRepository(db)
        user = user_repo.get_user(user_id)
        if not user:
            user_repo.get_or_create_user(userid=user_id, username=username)
            db.commit()
            return True  # user created
        return False  # user already existed
    except Exception as e:
        db.rollback()
        return False
