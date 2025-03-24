import datetime
import logging
from uuid import UUID

from crud.bookings import BookingRepository
from database.session import get_db
from fastapi import Depends, HTTPException
from models.booking import Booking
from models.enums import BookingStatusEnum
from schemas.booking import BookingCreate, BookingResponse
from sqlalchemy.orm import Session
from utils.google_calendar import (
    NURBURGRING_CALENDAR_ID,
    check_date_availability,
    service,
)
from utils.booking_utils import (
    check_car_availability,
    add_to_calendar,
)
from utils.voucher_utils import validate_voucher
from utils.exceptions import (
    BookingNotFoundException,
    GoogleCalendarException,
    ResourceUnavailableException,
    BookingStatusException,
    VoucherValidationException,
)

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def check_track_availability(self, date: str) -> dict:
        """Check if the track is open on a specific date using Google Calendar data"""
        return check_date_availability(date)

    def check_car_availability(self, car_id: UUID, date: str, hour: str) -> bool:
        """Check if a specific car is available on the requested date and hour"""
        return check_car_availability(self.db, car_id, date, hour)

    def create_temporary_booking(self, booking_data: BookingCreate) -> BookingResponse:
        if not booking_data.booking_time:
            raise HTTPException(
                status_code=400, detail="Booking time must be provided for booking."
            )

        driving_date = (
            booking_data.booking_time.date().isoformat()
        )  # Extract YYYY-MM-DD
        driving_hour = booking_data.booking_time.strftime("%H:%M")  # Extract HH:MM

        # Check track availability for the driving date
        track_availability = self.check_track_availability(driving_date)

        if track_availability.get("status") != "open":
            raise ResourceUnavailableException(
                resource_type="Track",
                detail=f"The track is not open on the selected booking date ({driving_date}).",
            )

        # Check car availability for the driving date and time
        if not self.check_car_availability(
            booking_data.car_id, driving_date, driving_hour
        ):
            raise ResourceUnavailableException(
                resource_type="Car",
                detail=f"The selected car is not available for this time slot ({driving_date} {driving_hour}).",
            )

        booking_dict = booking_data.model_dump()
        booking_dict.update(
            {
                "status": BookingStatusEnum.TEMPORARY_HOLD,
                "hold_placed_at": datetime.datetime.now(datetime.timezone.utc),
                "hold_expires_at": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=30),
            }
        )

        booking_repo = BookingRepository(self.db)
        booking = booking_repo.create_booking(BookingCreate(**booking_dict))

        return BookingResponse.model_validate(booking)

    def confirm_booking(self, booking_id: UUID) -> BookingResponse:
        booking = self.db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise BookingNotFoundException(booking_id=booking_id)

        if booking.status.value != BookingStatusEnum.TEMPORARY_HOLD.value:
            raise BookingStatusException(
                current_status=booking.status.value,
                target_status=BookingStatusEnum.CONFIRMED.value,
            )

        booking.status = BookingStatusEnum.CONFIRMED.value
        booking.payment_completed_at = datetime.datetime.now(datetime.timezone.utc)

        # Add the booking to Google Calendar
        try:
            add_to_calendar(self.db, booking)
        except GoogleCalendarException as e:
            logger.error("Failed to add booking to calendar: %s", e)

        self.db.commit()
        self.db.refresh(booking)

        return BookingResponse.model_validate(booking)

    def cleanup_expired_bookings(self):
        """Clean up expired temporary holds and pending payments"""
        now = datetime.datetime.now(datetime.timezone.utc)

        expired_holds = (
            self.db.query(Booking)
            .filter(
                Booking.status == BookingStatusEnum.TEMPORARY_HOLD,
                Booking.hold_expires_at < now,
            )
            .all()
        )

        for booking in expired_holds:
            booking.status = BookingStatusEnum.EXPIRED.value
            booking.cancellation_reason = "Hold period expired"

        self.db.commit()

    def validate_voucher(self, code: str) -> bool:
        try:
            __voucher = validate_voucher(code, self.db)
            return True
        except VoucherValidationException:
            return False

    def check_for_calendar_conflicts(self, car_id, booking_time, duration_hours=2):
        """Check for conflicting calendar events (simplified alternative to check_car_availability)"""
        start_time = booking_time.isoformat()
        end_time = (booking_time + datetime.timedelta(hours=duration_hours)).isoformat()

        try:
            events = (
                service.events()
                .list(
                    calendarId=NURBURGRING_CALENDAR_ID,
                    timeMin=start_time,
                    timeMax=end_time,
                    q=f"Car ID: {car_id}",
                )
                .execute()
            )
            return len(events.get("items", [])) > 0
        except GoogleCalendarException as e:
            logger.error("Error checking calendar conflicts: %s", e)
            return True
