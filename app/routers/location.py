from fastapi import APIRouter
from schemas.location import LocationResponse
from dependencies.database import db_dependency
from typing import List
from services.location import LocationService
router = APIRouter(prefix="/location", tags=["Locations"])
locationService=LocationService(db_dependency)
@router.get("/locations/", response_model=List[LocationResponse])
def read_locations( limit: int = 10):
    locations = locationService.get_locations( limit=limit)
    return locations

