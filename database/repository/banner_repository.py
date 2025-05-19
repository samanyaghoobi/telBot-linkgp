from sqlalchemy.orm import Session
from database.models.banner import Banner  

class BannerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Banner).all()

    def get_by_id(self, banner_id: int):
        return self.db.query(Banner).filter(Banner.id == banner_id).first()

    def create(self, banner_data: dict):
        banner = Banner(**banner_data)
        self.db.add(banner)
        self.db.commit()
        self.db.refresh(banner)
        return banner

    def update(self, banner_id: int, updates: dict):
        banner = self.get_by_id(banner_id)
        if not banner:
            return None
        for key, value in updates.items():
            setattr(banner, key, value)
        self.db.commit()
        self.db.refresh(banner)
        return banner

    def delete(self, banner_id: int):
        banner = self.get_by_id(banner_id)
        if banner:
            self.db.delete(banner)
            self.db.commit()
        return banner
