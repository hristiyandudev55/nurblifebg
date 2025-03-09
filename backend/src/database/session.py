from sqlalchemy import create_engine, Column
from sqlalchemy.orm import sessionmaker
from core.config import DB_URL

from models.base import Base

DATABASE_URL = DB_URL

engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
Session = sessionmaker(autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
