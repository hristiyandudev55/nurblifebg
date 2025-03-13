from typing import List
from uuid import UUID


from crud.hotels import HotelRepository
from database.session import get_db
from fastapi import APIRouter, Depends
from models.hotel import Hotel
from schemas.hotel import (
    AddHotel,
    HotelResponse,
    UpdateHotel,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=HotelResponse, status_code=200)
def add_hotel(hotel: AddHotel, db: Session = Depends(get_db)):
    """
    Create a new hotel.

    - **hotel**: Hotel data to be created.

    Args:
        hotel (AddHotel): Hotel data to be added.
        db (Session): Database session.

    Returns:
        HotelResponse: The created hotel data.
    """
    hotel_repo = HotelRepository(db_session=db)
    return hotel_repo.add(hotel=hotel)


@router.get("/{hotel_id}", response_model=HotelResponse, status_code=200)
def get_hotel_by_id(hotel_id: UUID, db: Session = Depends(get_db)):
    """
    Get a hotel by its ID.

    Args:
        hotel_id (UUID): The unique identifier of the hotel.
        db (Session): Database session.

    Returns:
        HotelResponse: The hotel data for the specified hotel ID.

    Raises:
        HTTPException: If the hotel with the given ID is not found.
    """
    hotel_repo = HotelRepository(db_session=db)
    return hotel_repo.get_hotel_by_id(hotel_id=hotel_id)


@router.get("/", response_model=List[HotelResponse], status_code=200)
def get_all_hotels(db: Session = Depends(get_db)):
    """
    Get a list of all hotels in the database.

    Args:
        db (Session): Database session.

    Returns:
        List[HotelResponse]: A list of all hotels in the database.
    """
    _hotel_repo = HotelRepository(db_session=db)
    db_hotels = db.query(Hotel).all()

    return [HotelResponse.model_validate(hotel) for hotel in db_hotels]


@router.patch("/{hotel_id}", response_model=HotelResponse, status_code=200)
def update_hotel(hotel_id: UUID, hotel: UpdateHotel, db: Session = Depends(get_db)):
    """
    Update a hotel by its ID.

    - **hotel_id**: ID of the hotel to be updated.
    - **hotel**: Updated data for the hotel.

    Args:
        hotel_id (UUID): The unique identifier of the hotel to be updated.
        hotel (UpdateHotel): The data to update the hotel.
        db (Session): Database session.

    Returns:
        HotelResponse: The updated hotel data.

    Raises:
        HTTPException: If the hotel with the given ID is not found or if the update fails.
    """
    hotel_repo = HotelRepository(db_session=db)
    return hotel_repo.update(hotel_id=hotel_id, hotel=hotel)


@router.delete("/{hotel_id}", status_code=200)
def delete_hotel(hotel_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a hotel by its ID.

    - **hotel_id**: ID of the hotel to be deleted.

    Args:
        hotel_id (UUID): The unique identifier of the hotel to be deleted.
        db (Session): Database session.

    Returns:
        dict: A message indicating that the hotel has been successfully deleted.

    Raises:
        HTTPException: If the hotel with the given ID is not found or if the deletion fails.
    """
    hotel_repo = HotelRepository(db_session=db)
    return hotel_repo.delete(hotel_id=hotel_id)
