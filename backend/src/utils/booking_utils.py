import logging
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.booking import Booking
from models.car import Car
from models.enums import BookingStatusEnum
from database.session import get_db
from utils.scheduler import scheduler
from utils.google_calendar import service
from core.config import NURB_CALENDAR_ID

logger = logging.getLogger(__name__)

#FIXME - statuses
@scheduler.scheduled_job("interval", minutes=5)
def cleanup_expired_bookings():
    """Cleanup expired bookings and failed payments"""
    db = next(get_db())
    try:
        now = datetime.utcnow()

        # Find all expired temporary holds
        expired_holds = (
            db.query(Booking)
            .filter(
                Booking.status == BookingStatusEnum.TEMPORARY_HOLD,
                Booking.hold_expires_at < now,
            )
            .all()
        )

        for booking in expired_holds:
            booking.status = BookingStatusEnum.EXPIRED # type: ignore

        # Find all failed payments
        expired_payments = (
            db.query(Booking)
            .filter(
                Booking.status == BookingStatusEnum.PENDING_PAYMENT,
                Booking.hold_expires_at < now,
            )
            .all()
        )

        for booking in expired_payments:
            booking.status = BookingStatusEnum.PAYMENT_FAILED # type: ignore

        db.commit()
        logger.info(
            f"Cleaned up {len(expired_holds)} expired holds and {len(expired_payments)} failed payments: %s")
    except HTTPException as e:
        db.rollback()
        logger.error("Error cleaning up expired bookings: %s", e)
    finally:
        db.close()


def check_car_availability(db: Session, car_id: UUID, date: str, hour: str) -> bool:
    """Check if a specific car is available on the requested booking date and hour"""
    try:
        booking_datetime = datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H:%M")

        conflicting_bookings = (
            db.query(Booking)
            .filter(
                Booking.car_id == car_id,
                Booking.booking_time
                <= booking_datetime + timedelta(hours=2),  # End time of requested slot
                Booking.booking_time + timedelta(hours=2)
                >= booking_datetime,  # Start time of requested slot
                Booking.status.in_(
                    [
                        BookingStatusEnum.TEMPORARY_HOLD,
                        BookingStatusEnum.PENDING_PAYMENT,
                        BookingStatusEnum.CONFIRMED,
                    ]
                ),
            )
            .count()
        )

        return conflicting_bookings == 0
    except Exception as e: #FIXME 
        logger.error("Error checking car availability: %s", e)
        return False


def has_calendar_event(booking_id: UUID) -> bool:
    """Check if a booking already has a calendar event"""
    try:
        events = (
            service.events()
            .list(
                calendarId=NURB_CALENDAR_ID,
                q=str(booking_id),
                timeMin=datetime.utcnow().isoformat() + "Z",
            )
            .execute()
        )

        return len(events.get("items", [])) > 0
    except HTTPException as e:
        logger.error("Error checking calendar event: %s", e)
        return False


def add_to_calendar(db: Session, booking: Booking) -> bool:
    """Add a booking to Google Calendar"""
    try:
        car = db.query(Car).filter(Car.id == booking.car_id).first()
        car_name = f"{car.make} {car.model}" if car else "Unknown Car"

        event = {
            "summary": f"Booking: {car_name} - {booking.full_name}",
            "description": f"Booking ID: {booking.id}\nLaps: {booking.laps}\nPackage: {booking.package.value}\nContact: {booking.email}, {booking.phone_number}",
            "start": {
                "dateTime": booking.booking_time.isoformat(),
                "timeZone": "Europe/Berlin",
            },
            "end": {
                "dateTime": (booking.booking_time + timedelta(hours=2)).isoformat(),
                "timeZone": "Europe/Berlin",
            },
            "colorId": "11",
        }

        logger.info(f"Adding event to calendar for booking {booking.id}: %s")
        response = (
            service.events()
            .insert(calendarId=NURB_CALENDAR_ID, body=event)
            .execute()
        )
        logger.info(f"Event created successfully: {response.get('id')}: %s")
        return True
    except Exception as e: #FIXME
        logger.error("Failed to add booking to calendar: %s", e)
        return False


@scheduler.scheduled_job("interval", hours=1)
def sync_bookings_with_calendar():
    """Sync confirmed bookings with Google Calendar"""
    db = next(get_db())
    try:
        # Get all confirmed bookings
        bookings = (
            db.query(Booking)
            .filter(
                Booking.status == BookingStatusEnum.CONFIRMED,
            )
            .all()
        )

        for booking in bookings:
            if not has_calendar_event(booking.id):
                logger.info(f"Syncing booking {booking.id} to calendar: %s")
                add_to_calendar(db, booking)

        logger.info(f"Calendar sync completed for {len(bookings)} bookings: %s")
    except Exception as e: #FIXME 
        logger.error("Error syncing bookings with calendar: %s", e)
    finally:
        db.close()
