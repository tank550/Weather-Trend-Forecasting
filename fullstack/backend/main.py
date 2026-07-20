from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import db.model
from db.database import check_connection, engine, Base
from controller.geocoding_controller import geocoding_router
from controller.weather_controller import weather_router

app = FastAPI(title="Weather Trend Forecasting API", version="1.0.0")

#Base.metadata.create_all(bind=engine)


@app.get("/health/db")
def check_db():
    if check_connection():
        try:
            Base.metadata.create_all(bind=engine)
            return {"db_status": "connected"}
        except Exception as e:
            print(f"Failed to create tables: {e}")
            return {"db_status": "not connected"}
    return {"db_status": "not connected"}

app.include_router(geocoding_router)
app.include_router(weather_router)