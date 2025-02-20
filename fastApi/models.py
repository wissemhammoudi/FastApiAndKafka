from sqlalchemy import String, ForeignKey,BIGINT
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship,registry
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from typing import Optional

class Base(DeclarativeBase):

    pass



class Location(Base):
    __tablename__ = 'Location'
    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)


    # Relationship to Weather
    weather: Mapped[Optional["Weather"]] = relationship("Weather", back_populates="location", uselist=False)

    def __repr__(self) -> str:
        return f"Location(id={self.location_id!r}, name={self.name!r}, country={self.country!r})"


class Weather(Base):
    __tablename__ = 'Weather'
    weather_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("Location.location_id"), nullable=False)
    
    # Weather data fields
    observation_time: Mapped[str] = mapped_column(String(255), nullable=False)
    temperature: Mapped[int] = mapped_column(Integer, nullable=False)
    weather_descriptions: Mapped[list] = mapped_column(String(255), nullable=True)
 

    # Relationship to Location
    location: Mapped["Location"] = relationship("Location", back_populates="weather")

    def __repr__(self) -> str:
        return f"Weather(id={self.weather_id!r}, location_id={self.location_id!r}, temperature={self.temperature!r})"
