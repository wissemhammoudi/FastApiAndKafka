from sqlalchemy.orm import Session
from models.weather import Weather 


class WeatherService:
    def __init__(self,db:Session):
        self.db=db
    def get_weathers(self, limit: int = 10):
        return self.db.query(Weather).limit(limit).all()

