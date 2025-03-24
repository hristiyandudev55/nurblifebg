import datetime
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base import Base, BaseMixin
from models.enums import BookingStatusEnum, Package, Trace


class Booking(Base, BaseMixin):
    __tablename__ = "booking"
    
    car_id = Column(UUID(as_uuid=True), ForeignKey("cars.id"))
    status = Column(Enum(BookingStatusEnum), default=BookingStatusEnum.TEMPORARY_HOLD)
    package = Column(Enum(Package))  # basic / premium
    laps = Column(Integer, nullable=False, default=2)
    booked_at = Column(DateTime, default=datetime.datetime.utcnow)  # Booking date
    booking_time = Column(DateTime, nullable=False)  # Booking slot for driving
    price_for_lap = Column(Float, default=30.0)  # Total price for a lap

    # VOUCHER IF APPLICABLE
    voucher_id = Column(UUID(as_uuid=True), ForeignKey("vouchers.id"), nullable=True)

    # CUSTOMER DETAILS
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    comment = Column(String(255))

    # ADDITIONAL TRACKING FIELDS
    hold_placed_at = Column(DateTime, nullable=True)
    hold_expires_at = Column(DateTime, nullable=True)
    payment_initiated_at = Column(DateTime, nullable=True)
    payment_completed_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(String, nullable=True)
    trace = Column(Enum(Trace), nullable=True)
    extra_driver = Column(Boolean, nullable=False, default=False)
    video_record = Column(Boolean, nullable=False, default=False)
    excess_reduction = Column(Boolean, nullable=False, default=False)


    car = relationship("Car", back_populates="bookings")
    extras = relationship("Extra", back_populates="booking")
    voucher = relationship("Voucher", back_populates="bookings")