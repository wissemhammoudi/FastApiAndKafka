from fastapi import APIRouter
from sqlalchemy.orm import Session
from services import weather
from schemas.weather import WeatherResponse
from dependencies.database import db_dependency
from typing import List
from services.weather import WeatherService
router = APIRouter(prefix="/Weather", tags=["Weather"])
weatherService=WeatherService(db_dependency)
@router.get("/weathers/", response_model=List[WeatherResponse])
def read_weathers( limit: int = 10):
    weathers = weatherService.get_weathers(limit=limit)
    return weathers

