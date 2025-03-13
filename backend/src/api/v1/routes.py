from fastapi import APIRouter
from api.v1.endpoints import (
    cars,
    hotels,
)

api_router = APIRouter()

api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
api_router.include_router(hotels.router, prefix="/hotels", tags=["hotels"])