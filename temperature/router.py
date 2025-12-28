from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from dependencies import get_db
from temperature.schemas import TemperatureBase, TemperatureRead, TemperatureCreate
from temperature.crud import create_temperatures, get_temperatures_list, get_temperature_by_city_id

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

@router.get("/")
def read_temperatures(db: Session = Depends(get_db)):
    return get_temperatures_list(db)

@router.delete("/{city_id}", response_model=TemperatureRead)
def retrieve_temperature_for_single_city_endpoint(city_id: int, db: Session = Depends(get_db)):
    result = get_temperature_by_city_id(db, city_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )
    return result


@router.post("/create", response_model=TemperatureRead)
def create_temperature_endpoint(temperature: TemperatureCreate, db: Session = Depends(get_db)):
    return create_temperatures(db, temperature)