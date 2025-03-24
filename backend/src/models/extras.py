from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.base import Base, BaseMixin
from sqlalchemy.dialects.postgresql import UUID  # Changed import


class Extra(Base, BaseMixin):
    __tablename__ = "extras"  # Експлицитно задаване на име на таблицата
    booking_id = Column(UUID(as_uuid=True), ForeignKey("booking.id"))
    video_record = Column(Boolean, default=False)
    second_driver = Column(Boolean, default=False)
    insurance = Column(Boolean, default=False)

    booking = relationship("Booking", back_populates="extras")
