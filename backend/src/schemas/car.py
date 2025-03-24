from typing import Optional
from uuid import UUID

from models.enums import CarGearboxEnum, DriveTypeEnum, RollcageTypeEnum, SeatsCountEnum
from pydantic import BaseModel, field_validator, model_validator


def validate_horsepower(cls, v, values):
    if v <= 0:
        raise ValueError("Horsepower must be positive")
    return v


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

    @field_validator("hp", "nm", "price_for_lap", "weight", "acceleration", mode="before")
    @classmethod
    def validate_positive_values(cls, v, field):
        if v <= 0:
            raise ValueError(f"{field.name} must be positive number.")
        return v

    @model_validator(mode="after")
    def validate_hp_vs_nm(self):
        if isinstance(self, CarCreate):
            if self.nm is not None and self.hp is not None:
                if self.nm < self.hp:
                    raise ValueError(
                        f"Torque {self.nm} must be greater than or equal to horsepower {self.hp}."
                    )
        return self


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
