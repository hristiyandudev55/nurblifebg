from typing import Optional
from uuid import UUID

from models.enums import CarGearboxEnum, DriveTypeEnum, RollcageTypeEnum, SeatsCountEnum
from pydantic import BaseModel


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}

class CarCreate(BaseConfig):
    image: str
    make: str
    model: str
    engine_type: str
    hp: int
    nm: int
    acceleration: float
    gearbox: CarGearboxEnum
    drive: DriveTypeEnum
    weight: int
    suspension_type: str
    brakes_type: str
    wheels: str
    tyres_type: str
    seats_type: str
    harness_type: str
    rollcage_type: RollcageTypeEnum
    price_for_lap: int
    seats_count: SeatsCountEnum

class CarResponse(CarCreate):
    id: UUID

class CarUpdate(CarCreate):
    image: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    engine_type: Optional[str] = None
    hp: Optional[int] = None
    nm: Optional[int] = None
    acceleration: Optional[float] = None
    gearbox: Optional[CarGearboxEnum] = None
    drive: Optional[DriveTypeEnum] = None
    weight: Optional[int] = None
    suspension_type: Optional[str] = None
    brakes_type: Optional[str] = None
    wheels: Optional[str] = None
    tyres_type: Optional[str] = None
    seats_type: Optional[str] = None
    harness_type: Optional[str] = None
    rollcage_type: Optional[RollcageTypeEnum] = None
    price_for_lap: Optional[int] = None
    seats_count: Optional[SeatsCountEnum] = None
