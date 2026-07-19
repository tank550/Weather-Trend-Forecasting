from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field



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



class CurrentWeatherQuery(BaseModel):
    location: str | None = Field(default=None, description="City name or zip code")
    lat: float | None = None
    lon: float | None = None
