from datetime import datetime, timedelta

from models.base import Base, BaseMixin
from models.enums import VoucherStatusEnum
from sqlalchemy import Column, DateTime, Enum, Integer, String, func


class Voucher(Base, BaseMixin):
    code = Column(
        String, nullable=False, unique=True
    )  # Unique code that will be auto generated
    amount = Column(Integer, nullable=False)
    issued_at = Column(DateTime, default=func.now)
    expiration_data = Column(
        DateTime, default=lambda: datetime.now() + timedelta(days=180)
    )
    status = Column(
        Enum(VoucherStatusEnum), default="active_voucher"
    )
    used_on = Column(DateTime, nullable=False)
