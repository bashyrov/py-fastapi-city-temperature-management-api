import asyncio
import datetime
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session
import httpx
from temperature import schemas
from temperature.models import Temperature
from city.models import City as city_model


def get_temperatures_list(
        db: Session,
        skip: int = 0,
        limit: int = 100
):
    return db.query(Temperature).offset(skip).limit(limit).all()


def create_temperatures(
        db: Session,
        temperature: schemas.TemperatureCreate
) -> Temperature:
    db_temperature = Temperature(**temperature.model_dump())
    db.add(db_temperature)
    db.commit()
    db.refresh(db_temperature)
    return db_temperature


def get_temperature_by_city_id(
        db: Session, city_id: int
) -> list[Type[Temperature]] | None:
    return db.query(
        Temperature
    ).filter(
        Temperature.city_id == city_id
    ).all()


async def fetch_temperature_for_city(
        client: httpx.AsyncClient,
        city_name: str
) -> tuple | None:
    API_KEY = "1f12317ca119994272713be2a5bef75a"
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("main") or "temp" not in data["main"]:
            print(f"{city_name}: temperature data not found")
            return city_name, None
        return city_name, data["main"]["temp"]

    except Exception as e:
        print(f"{city_name}: error {e}")
        return city_name, None


async def update_temperature_for_all_cities(
        db: Session
) -> bool | None:
    cities_list = db.scalars(
        select(city_model.name)
    ).all()

    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [
            fetch_temperature_for_city(client, city)
            for city in cities_list
        ]
        results = await asyncio.gather(*tasks)

    for city, temp in results:
        print(city, temp)
        if temp is not None:
            city_record = db.query(
                city_model
            ).filter(
                city_model.name == city
            ).first()
            if city_record:
                new_temp = Temperature(
                    city_id=city_record.id,
                    date_time=datetime.datetime.now(),
                    temperature=temp
                )
                db.add(new_temp)
    db.commit()
    return True
