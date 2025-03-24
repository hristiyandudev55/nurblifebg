from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from models.base import Base


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class AddHotel(BaseConfig):
    image: str
    name: str
    link_to_hotel: str
    distance_from_track: float  # distance in km


class HotelResponse(AddHotel):
    id: UUID


class UpdateHotel(BaseConfig):
    image: Optional[str] = None
    name: Optional[str] = None
    link_to_hotel: Optional[str] = None
    distance_from_track: Optional[float] = None
