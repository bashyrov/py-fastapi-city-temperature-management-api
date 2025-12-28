from city.router import router as city_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(city_router)