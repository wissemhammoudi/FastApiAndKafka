from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from typing import Optional


class Weather(Base):
    __tablename__ = 'Weather'
    weather_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("Location.location_id"), nullable=False)
    
    observation_time: Mapped[str] = mapped_column(String(255), nullable=False)
    temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    weather_descriptions: Mapped[list] = mapped_column(String(255), nullable=True)
 

    location: Mapped["Location"] = relationship("Location", back_populates="weather")

    def __repr__(self) -> str:
        return f"Weather(id={self.weather_id!r}, location_id={self.location_id!r}, temperature={self.temperature!r})"



class Location(Base):
    __tablename__ = 'Location'
    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    
    weather: Mapped[Optional["Weather"]] = relationship("Weather", back_populates="location", uselist=False)

    def __repr__(self) -> str:
        return f"Location(id={self.location_id!r}, name={self.name!r}, country={self.country!r})"

