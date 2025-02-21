from sqlalchemy import String
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from typing import Optional
from .weather import Weather



class Location(Base):
    __tablename__ = 'Location'
    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(255), nullable=False)


    # Relationship to Weather
    weather: Mapped[Optional["Weather"]] = relationship("Weather", back_populates="location", uselist=False)

    def __repr__(self) -> str:
        return f"Location(id={self.location_id!r}, name={self.name!r}, country={self.country!r})"

