import logging
from functools import lru_cache
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
from models.car import Car
from schemas.car import CarCreate, CarResponse, CarUpdate
from utils.transaction_context import transaction_context

logger = logging.getLogger(__name__)


class BaseRepository(ABC):
    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id):
        pass

    @abstractmethod
    def update(self, entity_id, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass


class CarRepository(BaseRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    @lru_cache(maxsize=25)
    def get_car_by_id(self, entity_id: UUID) -> Car:
        """
        Method to get the car by ID.

        Args:
            car_id (UUID): ID of the car.

        Returns:
            Car: Car object.

        Raises:
            HTTPException: If car not found.
        """
        db_car = self.db.query(Car).filter(Car.id == entity_id).first()

        if not db_car:
            error_message = f"Car with ID {entity_id} does not exist."
            logger.error(error_message)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_message)

        return db_car

    def create(self, entity: CarCreate) -> CarResponse:
        """
        Method for creating a new car record in the db.

        Args:
            car_data(CarCreate): The data for the car to be created.
            db(Session): The database session.

        Returns:
            CarResponse: The created car data.

        Raises:
            HTTPException: If there is an integrity error (status code 400)
            or a general database error (status code 500).
        """
        try:
            with transaction_context(self.db):
                db_car = Car(**entity.model_dump())
                self.db.add(db_car)


            self.db.refresh(db_car)
            return CarResponse.model_validate(db_car)

        except IntegrityError as e:
            logger.error("Integrity error creating car: %s", e)
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Integrity error: Duplicate entry or constraint violation.",
            ) from e

        except SQLAlchemyError as e:
            logger.error("Database error creating car: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error.",
            ) from e

    def get(self, entity_id: UUID) -> CarResponse:
        db_car = self.get_car_by_id(entity_id)

        return CarResponse.model_validate(db_car)

    def update(self, entity_id: UUID, entity: CarUpdate) -> CarResponse:
        try:
            with transaction_context(self.db):
                self.get_car_by_id.cache_clear()
                db_car = self.get_car_by_id(entity_id)

                for key, value in entity.model_dump(exclude_unset=True).items():
                    setattr(db_car, key, value)

            return CarResponse.model_validate(db_car)

        except SQLAlchemyError as e:
            logger.error("Database error updating car: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error.",
            ) from e

    def delete(self, entity_id: UUID) -> dict:
        try:
            with transaction_context(self.db):
                db_car = self.get_car_by_id(entity_id)

                self.db.delete(db_car)
            return {"detail": f"Car with ID {entity_id} deleted successfully."}

        except SQLAlchemyError as e:
            logger.error("Database error deleting car: %s", e)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error.",
            ) from e
