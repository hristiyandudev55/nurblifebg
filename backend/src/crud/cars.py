import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from models.car import Car
from schemas.car import CarCreate, CarResponse, CarUpdate


logger = logging.getLogger(__name__)


def create_car(car_data: CarCreate, db: Session) -> CarResponse:
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
        db_car = Car(**car_data.model_dump())
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return CarResponse.model_validate(db_car)
    except IntegrityError as e:
        db.rollback()
        logger.error("Integrity error creating car: %s", e)
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Integrity error: Duplicate entry or constraint violation.",
        ) from e
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Database error creating car: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error.") from e
