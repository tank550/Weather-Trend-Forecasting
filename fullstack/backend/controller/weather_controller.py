from fastapi import APIRouter, HTTPException, Query

from model.weather_models import OpenMeteoForecastResponse
from service.weather_service import open_meteo_service

weather_router = APIRouter(
    prefix="/weather", 
    tags=["weather"],
    responses={502: {"description": ""
    "Bad Gateway - Open-Meteo service unavailability.   "}},
    )


@weather_router.get("/current", response_model=OpenMeteoForecastResponse)
async def get_current_weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
) -> OpenMeteoForecastResponse:
  
    try:
        return await open_meteo_service.fetch_forecast(latitude=lat, longitude=lon)
    except HTTPException as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc