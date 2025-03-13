from sqlalchemy import Boolean, Column, Integer, String, Enum, Float
from models.base import Base, BaseMixin
from models.enums import CarGearboxEnum, DriveTypeEnum, RollcageTypeEnum, SeatsCountEnum


class Car(Base, BaseMixin):
    """
    Database model representing "cars" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:
        image (str): URL or path to the car image.
        make (str): Manufacturer of the car.
        model (str): Model of the car.
        engine_type (str): Engine specifications (example: 2.0-4cyl turbo).
        hp (int): Horsepower of the car.
        nm (int): Torque in Newton meters.
        acceleration (float): Acceleration time from 0 to 100 km/h in seconds.
        gearbox (CarGearboxEnum): Type of gearbox (e.g., manual, automatic).
        drive (str): Drive type (e.g., AWD, FWD, RWD).
        weight (int): Weight of the car in kilograms.
        suspension_type (str): Type of suspension (e.g., stock, HKS, Bilstein).
        brakes_type (str): Type of brakes (e.g., endurance, performance).
        wheels (str): Type of wheels (e.g., Pro Track ONE 18x8).
        tyres_type (str): Type of tyres (e.g., NANKANG NS2-R).
        seats_type (str): Type of seats (e.g., Recaro Pole Position).
        harness_type (str): Type of harness (e.g., 4 point harness).
        rollcage_type (str): Type of rollcage (e.g., Full Rollcage, semi, no).
        price_for_lap (int): Price for a lap in euros.
        seats_count (int): Number of seats in the car.
        in_repair_shop: Shows if the car is unavailable at the moment.
    """

    image = Column(String, nullable=False, unique=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    engine_type = Column(String, nullable=False)
    hp = Column(Integer, nullable=False)
    nm = Column(Integer, nullable=False)
    acceleration = Column(Float, nullable=False)
    gearbox = Column(Enum(CarGearboxEnum, native_enum=False), nullable=False)
    drive = Column(Enum(DriveTypeEnum), nullable=False)
    weight = Column(Integer, nullable=False)
    suspension_type = Column(String, nullable=False)
    brakes_type = Column(String, nullable=False)
    wheels = Column(String, nullable=False)
    tyres_type = Column(String, nullable=False)
    seats_type = Column(String, nullable=False)
    harness_type = Column(String, nullable=False)
    rollcage_type = Column(Enum(RollcageTypeEnum), nullable=False)
    price_for_lap = Column(Integer, nullable=False)
    seats_count = Column(Enum(SeatsCountEnum), nullable=False)
    in_repair_shop = Column(Boolean, nullable=False, default=False)
