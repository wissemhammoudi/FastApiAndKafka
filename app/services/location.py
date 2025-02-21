from sqlalchemy.orm import Session
from models.location import Location
class LocationService:
    def __init__(self, db: Session):
        self.db = db

    def get_locations(self, limit: int = 10):
        return self.db.query(Location).limit(limit).all()
