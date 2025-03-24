from datetime import datetime, timedelta

from models.base import Base, BaseMixin
from models.enums import VoucherStatusEnum
from sqlalchemy import Column, DateTime, Enum, Integer, String, func, true
from sqlalchemy.orm import relationship


class Voucher(Base, BaseMixin):
    __tablename__="vouchers"

    code = Column(
        String, nullable=False, unique=True
    )  # Unique code that will be auto generated
    amount = Column(Integer, nullable=False)
    issued_at = Column(DateTime, default=func.now)
    expiration_date = Column(
        DateTime, default=lambda: datetime.now() + timedelta(days=180)
    )
    status = Column(
        Enum(VoucherStatusEnum), default=VoucherStatusEnum.ACTIVE_VOUCHER
    )  # Използване на enum стойност, не string
    used_on = Column(DateTime, nullable=True)

    bookings = relationship("Booking", back_populates="voucher")
