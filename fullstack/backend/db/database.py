from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
# from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

from db.model import WeatherRequest

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")




# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def check_connection() -> bool: 
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Failed to connect: {e}")
        return False
    

def save_weather(data:WeatherRequest):
    try:
        with SessionLocal() as session:
            session.add(data)
            session.commit()
            session.refresh(data)
            return data
    except Exception as e:
        session.rollback()
        print(f"Failed to save weather data: {e}")
        return None