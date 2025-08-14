from sqlalchemy.orm import Session
from core.database import SessionLocal  
from typing import Annotated
from fastapi import Depends

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


