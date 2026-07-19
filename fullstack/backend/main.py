from fastapi import FastAPI
from controller.geocoding_controller import geocoding_router
from controller.weather_controller import weather_router

app = FastAPI(title="Weather Trend Forecasting API", version="1.0.0")


app.include_router(geocoding_router)
app.include_router(weather_router)