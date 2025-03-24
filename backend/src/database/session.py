from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Импортирайте Base
from models.base import Base

# Импортирайте всички модели в правилния ред
from models.car import Car 
from models.voucher import Voucher  # Първо Voucher, преди Booking
from models.booking import Booking  # След това Booking
from models.hotel import Hotel
from models.extras import Extra
# Други модели...

load_dotenv()

# Променете DATABASE_URL от postgres:// на postgresql://
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# За SQLite използвайте различни настройки
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from models.base import Base
    from models.car import Car 
    from models.voucher import Voucher  
    from models.hotel import Hotel
    from models.booking import Booking
    from models.extras import Extra
    
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
