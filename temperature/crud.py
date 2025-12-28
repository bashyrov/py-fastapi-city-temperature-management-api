from sqlalchemy.orm import Session
from temperature import schemas
from temperature.models import Temperature
from temperature.schemas import TemperatureRead


def get_temperatures_list(db: Session, skip:int=0, limit: int=100):
    return db.query(Temperature).offset(skip).limit(limit).all()


def create_temperatures(db: Session, temperature: schemas.TemperatureCreate) -> Temperature:
    db_temperature = Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature

def get_temperature_by_city_id(db: Session, city_id: int) -> TemperatureRead | None:
    return db.query(Temperature).filter(Temperature.city_id == city_id).first()
