from datetime import date
import json
import uuid

from fastapi import APIRouter, HTTPException, Query

from model.weather_models import OpenMeteoForecastResponse, WeatherCreate, WeatherUpdate
from service.export_service import export_response
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
    

@weather_router.post("/save")
async def save_weather(payload: WeatherCreate):  
    try:
        return await open_meteo_service.save_weather(latitude=payload.latitude, longitude=payload.longitude, start_date=payload.start_date, end_date=payload.end_date, country=payload.country, location_name=payload.location_name)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
@weather_router.get("/all")
def getallweather():
    try:
        return open_meteo_service.get_all_weather()
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@weather_router.get("/location")
def get_weather_by_location(lat: float = Query(..., ge=-90, le=90, description="Latitude"),
                            lon: float = Query(..., ge=-180, le=180, description="Longitude"),):
    try:
        return open_meteo_service.get_weather_by_location(latitude=lat, longitude=lon)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    
@weather_router.get("/date_range")
def get_weather_by_date_range(start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
                              end_date: date = Query(..., description="End date in YYYY-MM-DD format"),):
    try:
        return open_meteo_service.get_weather_by_date_range(start_date=start_date, end_date=end_date)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@weather_router.post("/explain")
async def weather_explain_by_llm(payload: OpenMeteoForecastResponse):
    try:
        return await open_meteo_service.weather_explain_by_llm(payload)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@weather_router.get("/{weather_id}")
def get_weather_by_id(weather_id: uuid.UUID):
    try:
        return open_meteo_service.get_weather_by_id(weather_id)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    

@weather_router.get("/export/all")
def Exportallweather(format:str=Query(description="Export format like csv or json")):
    try:
        data = open_meteo_service.get_all_weather()
        return export_response(data,format)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@weather_router.get("/export/location")
def export_weather_by_location(lat: float = Query(..., ge=-90, le=90, description="Latitude"),
                            lon: float = Query(..., ge=-180, le=180, description="Longitude"),
                            format:str=Query(description="Export format like csv or json")):
    try:
        data = open_meteo_service.get_weather_by_location(latitude=lat, longitude=lon)
        return export_response(data,format)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@weather_router.get("/export/date_range")
def export_weather_by_date_range(start_date: date = Query(..., description="Start date in YYYY-MM-DD format"),
                              end_date: date = Query(..., description="End date in YYYY-MM-DD format"),
                              format:str=Query(description="Export format like csv or json")):
    try:
        data = open_meteo_service.get_weather_by_date_range(start_date=start_date, end_date=end_date)
        return export_response(data,format)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@weather_router.delete("/{weather_id}")
def delete_weather_by_id(weather_id: uuid.UUID):
    try:
        return open_meteo_service.delete_weather_by_id(weather_id)
    except HTTPException as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@weather_router.patch("/{weather_id}")
async def update_weater_by_id(weather_id: uuid.UUID, payload: WeatherUpdate):
    try:
        return await open_meteo_service.update_weather(weather_id,payload)
    except HTTPException as exc :
        raise HTTPException(status_code=400, detail=str(exc)) from exc


