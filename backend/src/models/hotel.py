from sqlalchemy import Column, String, Float
from models.base import Base, BaseMixin


class Hotel(Base, BaseMixin):
    """
    Represents a hotel entity.

    Attributes:
        image (str): URL or path to the hotel's image. Must be unique and cannot be null.
        link_to_hotel (str): URL linking to the hotel's official website or booking page. 
                             Must be unique and cannot be null.
    """
    image = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    link_to_hotel = Column(String, nullable=False, unique=True)
    distance_from_track = Column(Float, nullable=False)
