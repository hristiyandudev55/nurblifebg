from typing import List
from uuid import UUID


from crud.cars import CarRepository
from database.session import get_db
from fastapi import APIRouter, Depends
from models.car import Car
from schemas.car import (
    CarCreate,
    CarResponse,
    CarUpdate,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=CarResponse, status_code=200)
def _create_car(car: CarCreate, db: Session = Depends(get_db)):
    """
    Create a new car with the provided information.

    - **car**: Car data to be created
    """
    car_repo = CarRepository(db_session=db)
    return car_repo.create(entity=car)


@router.get("/{car_id}", response_model=CarResponse, status_code=200)
def _get_car_by_id(car_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a car by its unique ID.

    Returns:
        CarResponse: The car object.
    """
    car_repo = CarRepository(db_session=db)
    return car_repo.get_car_by_id(entity_id=car_id)


@router.get("/", response_model=List[CarResponse], status_code=200)
def _get_all_cars(db: Session = Depends(get_db)):
    """
    Retrieve all cars stored in the database.

    Returns:
        List[CarResponse]: A list of CarResponse objects.
    """
    _car_repo = CarRepository(db_session=db)
    db_cars = db.query(Car).all()

    return [CarResponse.model_validate(car) for car in db_cars]


@router.patch("/{car_id}", response_model=CarResponse, status_code=200)
def update_car(car_id: UUID, car: CarUpdate, db: Session = Depends(get_db)):
    """
    Partially update a car by its ID.

    Returns:
        CarResponse: The updated car object.
    """
    car_repo = CarRepository(db_session=db)
    return car_repo.update(entity_id=car_id, entity=car)


@router.delete("/{card_id}", status_code=200)
def delete_car(car_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a car from database.

    Returns:
        Status code 200 if deletion is successfull.
    """
    car_repo = CarRepository(db_session=db)
    return car_repo.delete(entity_id=car_id)
