from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from .location import Location

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
