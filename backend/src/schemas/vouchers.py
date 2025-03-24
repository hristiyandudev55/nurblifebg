from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from models.enums import VoucherStatusEnum


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class VoucherDetails(BaseConfig):
    id: UUID
    code: str
    status: VoucherStatusEnum
    created_at: datetime
    expiration_date: datetime
