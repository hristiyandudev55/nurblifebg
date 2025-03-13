from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class AddHotel(BaseConfig):
    image: str
    name: str
    link: str
    distance_from_track: float  # distance in km


class HotelResponse(AddHotel):
    id: UUID


class UpdateHotel(AddHotel):
    image: Optional[str] = None
    name: Optional[str] = None
    link: Optional[str] = None
    distance_from_track: Optional[float] = None
