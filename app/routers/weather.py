from fastapi import APIRouter,Depends
from schemas.weather import WeatherResponse
from dependencies.database import get_db
from typing import List
from services.weather import WeatherService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/Weather", tags=["Weather"])
@router.get("/weathers/", response_model=List[WeatherResponse])
def read_weathers(limit: int = 10, db: Session = Depends(get_db)):  
    """Fetch weather data with a limit."""
    weather_service = WeatherService(db)  # Instantiate service inside the route
    return weather_service.get_weathers(limit=limit)