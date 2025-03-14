from sqlalchemy import Column, Integer, String, Date
from models.base import Base, BaseMixin


class User(Base, BaseMixin):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    postcode = Column(String, nullable=False)
    town = Column(String, nullable=False)
    comment = Column(String(255))
