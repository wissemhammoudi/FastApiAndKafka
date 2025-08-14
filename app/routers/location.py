from fastapi import APIRouter,Depends
from schemas.location import LocationResponse
from dependencies.database import get_db
from typing import List
from services.location import LocationService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/location", tags=["Locations"])

@router.get("/locations/", response_model=List[LocationResponse])
def read_locations( limit: int = 10, db: Session = Depends(get_db) ):
    locationService=LocationService(db)
    locations = locationService.get_locations( limit=limit)
    return locations

