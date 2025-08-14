from pydantic import BaseModel
from typing import  List


class WeatherResponse(BaseModel):
    weather_id: int
    location_id: int
    observation_time: str
    temperature: int
    weather_descriptions:str

    class Config:
        from_attributes = True  