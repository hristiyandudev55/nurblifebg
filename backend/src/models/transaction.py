from sqlalchemy import Column, Integer
from models.base import Base, BaseMixin


class Transaction(Base, BaseMixin):
    amount = Column(Integer, nullable=False)
