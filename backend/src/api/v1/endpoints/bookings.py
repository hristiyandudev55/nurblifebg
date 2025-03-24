import logging
from typing import List
from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.orm import Session
from database.session import get_db
from services.booking_service import BookingService
from src.crud.bookings import BookingRepository
from schemas.booking import BookingCreate, BookingResponse, BookingUpdate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/track-availability/{date}")
def check_track_availability(date: str, service: BookingService = Depends()):
    """
    Check if the track is open on a specific date
    Date format: YYYY-MM-DD
    """
    return service.check_track_availability(date)


@router.get("/car-availability/{car_id}/{date}/{hour}")
def check_car_availability(
    car_id: UUID, date: str, hour: str, service: BookingService = Depends()
):
    """
    Check if a car is available on a specific date and hour
    Date format: YYYY-MM-DD
    Hour format: HH:MM
    """
    is_available = service.check_car_availability(car_id, date, hour)
    return {"available": is_available}


@router.post("/", response_model=BookingResponse)
def create_booking(booking_data: BookingCreate, service: BookingService = Depends()):
    """
    Create a new booking (temporary hold)
    """
    return service.create_temporary_booking(booking_data)


@router.put("/{booking_id}/confirm", response_model=BookingResponse)
def confirm_booking(booking_id: UUID, service: BookingService = Depends()):
    """
    Confirm a booking after payment
    """
    return service.confirm_booking(booking_id)


@router.get("/", response_model=List[BookingResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    """
    Get all bookings with TEMPORARY_HOLD or PENDING_PAYMENT status
    """
    booking_repo = BookingRepository(db_session=db)
    return booking_repo.get_all_bookings()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: UUID, db: Session = Depends(get_db)):
    """
    Get a booking by ID
    """
    booking_repo = BookingRepository(db_session=db)
    return booking_repo.get_booking(booking_id)


@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: UUID, booking: BookingUpdate, db: Session = Depends(get_db)):
    """
    Update a booking by ID
    """
    booking_repo = BookingRepository(db_session=db)
    return booking_repo.update_booking(booking_id=booking_id, details=booking)


@router.delete("/{booking_id}")
def delete_booking(booking_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a booking by ID
    """
    booking_repo = BookingRepository(db_session=db)
    return booking_repo.delete_booking(booking_id=booking_id)
