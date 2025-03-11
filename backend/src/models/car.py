from fastapi import FastAPI
from sqlalchemy import UUID, Column, Integer, String, Enum, ForeignKey, Float, null
from sqlalchemy.orm import relationship
from models.base import Base, BaseMixin
from models.enums import CarGearboxEnum

class Car(Base, BaseMixin):
    """
    Database model representing "cars" table in the database.
    UUID and table name are inherited from BaseMixin.

    Attributes:

    """

    image = Column(String, nullable=False,unique=True)
    make = Column(String,nullable=False)
    model = Column(String,nullable=False)
    engine_type = Column(String,nullable=False) #(example: 2.0-4cyl turbo)
    hp = Column(Integer, nullable=False) #e.g 240 (horse power)
    nm = Column(Integer,nullable=False) #e.g 320 (NM)
    acceleration = Column(Float,nullable=False) #e.g - 6.5 (seconds)
    gearbox = Column(Enum(CarGearboxEnum, native_enum=False), nullable=False)
    drive = Column(String,nullable=False) #e.g AWD/FWD/RWD
    weight = Column(Integer,nullable=False) #e.g 1500 kg
    suspension_type = Column(String,nullable=False) #e.g stock/ HKS, bilstein, etc
    brakes_type = Column(String,nullable=False) #e.g endurance/performance
    wheels = Column(String,nullable=False) #e.g Pro Track ONE 18x8
    tyres_type = Column(String,nullable=False) #e.g NANKANG NS2-R
    seats_type = Column(String,nullable=False) #e.g Recaro Pole Position
    harness_type = Column(String,nullable=False) #e.g 4 point harness
    rollcage_type = Column(String,nullable=False) #e.g Full Rollcage/ semi/ no
    price_for_lap = Column(Integer,nullable=False) #e.g 100 euro
    seats_count = Column(Integer,nullable=False) #e.g 1/2/3  