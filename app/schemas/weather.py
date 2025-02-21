from pydantic import BaseModel
from typing import Optional, List


# Schema for response (includes all fields)
class WeatherResponse(BaseModel):
    weather_id: int
    location_id: int
    observation_time: str
    temperature: int
    weather_descriptions: Optional[List[str]] = None

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models