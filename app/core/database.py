from sqlalchemy import create_engine,URL
from sqlalchemy.orm import sessionmaker
from .config import Settings

settings = Settings()
url = URL.create(
    drivername= settings.DATABASE_NAME,
    username=settings.USERNAME,
    password=settings.PASSWORD,
    host=settings.HOST,
    port=settings.PORT,
    database=settings.DATABASE
)

engine=create_engine(url)
SessionLocal =sessionmaker(engine)
