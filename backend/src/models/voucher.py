from sqlalchemy import DateTime, Column, String, Integer, func
from models.base import Base, BaseMixin
from datetime import datetime, timedelta


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
        String, default="active"
    )  # TODO - Add Enum with statuses for vouchers >active/used/expired
    used_on = Column(DateTime, nullable=False)
