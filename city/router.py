from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from city.schemas import CityCreate, City
from city.crud import create_city

router = APIRouter(prefix="/cities", tags=["cities"])

@router.post("/create", response_model=City)
def create_city_endpoint(city: CityCreate, db: Session = Depends(get_db)):
    return create_city(db, city)
