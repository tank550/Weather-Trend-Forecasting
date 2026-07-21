from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, field_validator
from datetime import date



class CurrentUnits(BaseModel):
    time: str
    interval: str
    temperature_2m: str
    relative_humidity_2m: str
    apparent_temperature: str
    is_day: str
    wind_speed_10m: str
    wind_direction_10m: str
    wind_gusts_10m: str
    precipitation: str
    weather_code: str
    rain: str
    surface_pressure: str
    cloud_cover: str


class Current(BaseModel):
    time: int  # unixtime (timeformat=unixtime)
    interval: int
    temperature_2m: float
    relative_humidity_2m: int
    apparent_temperature: float
    is_day: int
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float
    precipitation: float
    weather_code: int
    rain: float
    surface_pressure: float
    cloud_cover: int



class HourlyUnits(BaseModel):
    time: str
    temperature_2m: str
    weather_code: str
    precipitation_probability: str


class Hourly(BaseModel):
    time: List[int]
    temperature_2m: List[float]
    weather_code: List[int]
    precipitation_probability: List[int]



class DailyUnits(BaseModel):
    time: str
    weather_code: str
    temperature_2m_max: str
    wind_speed_10m_max: str
    wind_gusts_10m_max: str
    wind_direction_10m_dominant: str


class Daily(BaseModel):
    time: List[int]
    weather_code: List[int]
    temperature_2m_max: List[float]
    wind_speed_10m_max: List[float]
    wind_gusts_10m_max: List[float]
    wind_direction_10m_dominant: List[int]



class OpenMeteoForecastResponse(BaseModel):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float

    current_units: CurrentUnits
    current: Current

    hourly_units: HourlyUnits
    hourly: Hourly

    daily_units: DailyUnits
    daily: Daily





class WeatherCreate(BaseModel):
    latitude: float
    longitude: float
    start_date: date
    end_date: date
    location_name: str
    country: str

    
    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        return v

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return v

    @field_validator("end_date")
    @classmethod
    def check_date_range(cls, end_date, info):
        start_date = info.data.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("end_date must be >= start_date")
        if start_date and (end_date - start_date).days > 16:
            raise ValueError("The date range cannot exceed 16 days (Open-Meteo API limit)")
        return end_date