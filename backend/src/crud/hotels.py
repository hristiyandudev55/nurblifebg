import logging
from abc import ABC, abstractmethod
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from models.hotel import Hotel
from schemas.hotel import AddHotel, HotelResponse, UpdateHotel
from utils.transaction_context import transaction_context

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    @abstractmethod
    def add(self, hotel):
        pass

    @abstractmethod
    def get(self, hotel_id):
        pass

    @abstractmethod
    def update(self, hotel_id, hotel):
        pass

    @abstractmethod
    def delete(self, hotel_id):
        pass


class HotelRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_hotel_by_id(self, hotel_id: UUID) -> Hotel:
        """ "
        Method to get the hotel by ID.

        Args:
            hotel_id (UUID): ID of the hotel.

        Returns:
            Hotel: Hotel object.

        Raises:
            HTTPException: If hotel not found.
        """
        db_hotel = self.db.query(Hotel).filter(Hotel.id == hotel_id).first()

        if not db_hotel:
            error_message = f"Hotel with ID {hotel_id} does not exists."
            logger.error(error_message)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_message)

        return db_hotel

    def add(self, hotel: AddHotel) -> HotelResponse:
        """ """
        try:
            with transaction_context(self.db):
                db_hotel = Hotel(**hotel.model_dump())
                self.db.add(db_hotel)
                self.db.refresh(db_hotel)

            return HotelResponse.model_validate(db_hotel)

        except IntegrityError as e:
            logger.error("Integity error adding hotel: %s", e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Integiry error: Duplicate entry or constrain violation.",
            ) from e

        except SQLAlchemyError as e:
            logger.error("Database error adding hotel: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error.",
            ) from e

    def get(self, hotel_id: UUID) -> HotelResponse:
        db_hotel = self.get_hotel_by_id(hotel_id)

        return HotelResponse.model_validate(db_hotel)

    def update(self, hotel_id: UUID, hotel: UpdateHotel):
        try:
            with transaction_context(self.db):
                db_hotel = self.get_hotel_by_id(hotel_id)

                for key, value in hotel.model_dump(exclude_unset=True).items():
                    setattr(db_hotel, key, value)

            return UpdateHotel.model_validate(db_hotel)

        except SQLAlchemyError as e:
            logger.error("Database error updating hotel: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from e

    def delete(self, hotel_id: UUID) -> dict:
        try:
            with transaction_context(self.db):
                db_hotel = self.get_hotel_by_id(hotel_id)

                self.db.delete(db_hotel)
            return {"detail": f"Hotel with ID {hotel_id} deleted successfully."}
        except SQLAlchemyError as e:
            logger.error("Datbase error deleting hotel: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from e
