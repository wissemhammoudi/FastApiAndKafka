from pydantic import BaseModel
from typing import Optional



class LocationResponse(BaseModel):
    location_id: int
    name: str
    country: str

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models