import logging
from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.booking import Booking
from models.enums import BookingStatusEnum
from schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from utils.exceptions import (
    BookingNotFoundException,
    DatabaseOperationException,
    ForeignKeyConstraintException,
    IntegrityConstraintException,
)
from utils.transaction_context import transaction_context

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    @abstractmethod
    def create_booking(self, car_id, date_time, customer_details):
        pass

    @abstractmethod
    def get_booking(self, booking_id):
        pass

    @abstractmethod
    def get_all_bookings(self):
        pass

    @abstractmethod
    def update_booking(self, booking_id, details):
        pass

    @abstractmethod
    def delete_booking(self, booking_id):
        pass


class BookingRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_booking_by_id(self, booking_id: UUID) -> Booking:
        """
        Method to get the booking by ID

        Args:
            booking_id (UUID): ID of the reservation.

        Returns:
            Booking: Booking object.

        Raises:
            HTTPException: If booking not found.
        """
        db_booking = self.db.query(Booking).filter(Booking.id == booking_id).first()

        if not db_booking:
            logger.error(f"Booking iwth ID {booking_id} does not exist.: %s")
            raise BookingNotFoundException(booking_id=booking_id)

        return db_booking

    def create_booking(self, booking_data: BookingCreate) -> BookingResponse:
        try:
            with transaction_context(self.db):
                booking = Booking(**booking_data.model_dump())
                self.db.add(booking)

            self.db.refresh(booking)
            return BookingResponse.model_validate(booking)

        except IntegrityError as e:
            error_msg = str(e)
            logger.error("Integrity error creating booking: %s", (error_msg))

            if "foreign key constraint" in error_msg.lower():
                raise ForeignKeyConstraintException(
                    detail=f"Foreign key constraint violation: {error_msg}",
                    context={"booking_data": booking_data.model_dump()},
                ) from e
            else:
                raise IntegrityConstraintException(
                    detail=f"Database integrity error: {error_msg}",
                    context={"booking_data": booking_data.model_dump()},
                ) from e

        except SQLAlchemyError as e:
            logger.error("Database error creating booking: %s", e)
            raise DatabaseOperationException(
                detail="Failed to create booking",
                context={"error": str(e), "booking_data": booking_data.model_dump()},
            ) from e

    def get_booking(self, booking_id: UUID) -> BookingResponse:
        db_booking = self.get_booking_by_id(booking_id)

        return BookingResponse.model_validate(db_booking)

    def get_all_bookings(self):
        db_bookings = (
            self.db.query(Booking)
            .filter(
                or_(
                    Booking.status == BookingStatusEnum.TEMPORARY_HOLD,
                    Booking.status == BookingStatusEnum.PENDING_PAYMENT,
                )
            )
            .all()
        )
        return [BookingResponse.model_validate(booking) for booking in db_bookings]

    def update_booking(self, booking_id: UUID, details: BookingUpdate):
        try:
            with transaction_context(self.db):
                db_booking = self.get_booking_by_id(booking_id)

                for key, value in details.model_dump(exclude_unset=True).items():
                    setattr(db_booking, key, value)

            return BookingResponse.model_validate(db_booking)

        except SQLAlchemyError as e:
            logger.error("Database error updating car: %s", e)
            raise DatabaseOperationException(
                detail="Failed to update booking",
                context={
                    "booking_id": str(booking_id),
                    "details": details.model_dump(),
                    "error": str(e),
                },
            ) from e

    def delete_booking(self, booking_id: UUID) -> dict:
        try:
            with transaction_context(self.db):
                db_booking = self.get_booking_by_id(booking_id)

                self.db.delete(db_booking)
            return {"detail": f"Booking with ID {booking_id} deleted successfully."}

        except SQLAlchemyError as e:
            logger.error("Database error deleting booking: %s", e)
            raise DatabaseOperationException(
                detail="Failed to delete booking",
                context={"booking_id": str(booking_id), "error": str(e)},
            ) from e
