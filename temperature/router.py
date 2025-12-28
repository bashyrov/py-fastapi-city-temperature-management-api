from fastapi import APIRouter

router = APIRouter(prefix="/temperatures", tags=["temperatures"])

@router.get("/")
def read_temperatures():
    return {"message": "List of temperatures"}