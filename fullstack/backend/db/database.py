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

def get_all_weather():
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).all()
            return weather_data
    except Exception as e:
        print(f"Failed to retrieve weather data: {e}")
        return None
    
def get_weather_by_id(weather_id):
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).filter(WeatherRequest.id == weather_id).first()
            return weather_data
    except Exception as e:
        print(f"Failed to retrieve weather data by ID: {e}")
        return None
    
def get_weather_by_location(latitude, longitude):
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).filter(
                WeatherRequest.latitude == latitude,
                WeatherRequest.longitude == longitude
            ).all()
            return weather_data
    except Exception as e:
        print(f"Failed to retrieve weather data by location: {e}")
        return None

def get_weather_by_date_range(start_date, end_date):
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).filter(
                WeatherRequest.start_date >= start_date.isoformat(),
                WeatherRequest.end_date <= end_date.isoformat()
            ).all()
            return weather_data
    except Exception as e:
        raise ValueError(f"Failed to retrieve weather data by date range: {e}")
        return None


def delete_weather_by_id(weather_id):
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).filter(WeatherRequest.id == weather_id).first()
            if weather_data:
                session.delete(weather_data)
                session.commit()
                return True
            else:
                return False
    except Exception as e:
        raise ValueError(f"Failed to delete weather data by ID: {e}")


def update_weather_by_id(weather_id, updated_data: WeatherRequest):
    try:
        with SessionLocal() as session:
            weather_data = session.query(WeatherRequest).filter(WeatherRequest.id == weather_id).first()
            if weather_data:
                for key, value in updated_data.__dict__.items():
                    if key != "_sa_instance_state" and value is not None:
                        setattr(weather_data, key, value)
                session.commit()
                session.refresh(weather_data)
                return weather_data
            else:
                return None
    except Exception as e:
        raise ValueError(f"Failed to update weather data by ID: {e}")