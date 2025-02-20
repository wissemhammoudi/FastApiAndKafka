from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker,Session
from typing import Annotated
from fastapi import Depends
# Database configuration
url = URL.create(
    drivername="postgresql+psycopg2",
    username="admin",
    password="admin",
    host="postgres",
    port=5432,
    database="weather_db"
)

engine=create_engine(url)
SessionLocal =sessionmaker(engine)
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]