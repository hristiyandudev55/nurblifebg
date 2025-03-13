from fastapi import APIRouter
from api.v1.endpoints import (
    cars,
)

api_router = APIRouter()

api_router.include_router(cars.router, prefix="/cars", tags=["cars"])
