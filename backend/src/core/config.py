import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", ""))

if not DB_URL:
    DB_URL = f"postgresql://{os.getenv('DB_USER')}:{DB_PASSWORD}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"
