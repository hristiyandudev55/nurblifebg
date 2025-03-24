from datetime import datetime
from typing import Optional
from uuid import UUID
import re

from pydantic import BaseModel, field_validator, EmailStr
from models.enums import BookingStatusEnum, Package, Trace


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True, "arbitrary_types_allowed": True}


class BookingDetails(BaseConfig):
    full_name: str
    email: EmailStr
    phone_number: str
    comment: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: str, info):
        digits_only = re.sub(r"\D", "", v)
        if len(digits_only) != 10:
            raise ValueError("Phone number must have exactly 10 digits")
        return digits_only


class BookingCreate(BaseConfig):
    car_id: UUID
    package: Package
    booked_at: datetime  # Time when the booking is made
    booking_time: datetime  # Time slot for driving
    laps: int
    price_for_lap: float
    voucher_id: Optional[UUID] = None
    full_name: str
    email: EmailStr
    phone_number: str
    comment: Optional[str] = None
    trace: Optional[Trace] = None
    extra_driver: Optional[bool] = False
    video_record: Optional[bool] = False
    excess_reduction: Optional[bool] = False

    @field_validator("video_record", "excess_reduction")
    @classmethod
    def validate_extras(cls, v, values):
        return v

    @field_validator("laps")
    @classmethod
    def validate_num_laps(cls, v, values):
        if v < 1:
            raise ValueError("Number of laps must be at least 1")
        return v


class BookingResponse(BaseConfig):
    id: UUID
    car_id: UUID
    status: BookingStatusEnum
    package: Package
    laps: int
    booking_time: datetime
    price_for_lap: float
    voucher_id: Optional[UUID] = None
    full_name: str
    email: EmailStr
    phone_number: str
    comment: Optional[str] = None
    hold_expires_at: Optional[datetime] = None


class BookingUpdate(BaseConfig):
    car_id: Optional[UUID] = None
    status: Optional[BookingStatusEnum] = None
    package: Optional[Package] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    extra_driver: Optional[bool] = None
    video_record: Optional[bool] = None
    excess_reduction: Optional[bool] = None
