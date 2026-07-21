"""
Service responsible solely for communicating with the Open-Meteo API
and parsing the response.
"""

from http.client import HTTPException

from db.model import WeatherRequest
from db.model import WeatherRequest
from model.weather_models import OpenMeteoForecastResponse
from service import any_url_check
from datetime import date
from db.database import save_weather

open_meteo_url = "https://api.open-meteo.com/v1/forecast"

# Fixed parameters for the Open-Meteo request (we do not want the user to be able to modify them)

daily_params = "weather_code,temperature_2m_max,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant"
hourly_params = "temperature_2m,weather_code,precipitation_probability"
current_params = (
    "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,"
    "wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,"
    "weather_code,rain,surface_pressure,cloud_cover"
)


class OpenMeteoService:
    """Wrapper around the Open-Meteo forecast API."""

    def __init__(self, timeout: float = 10.0):
        self._timeout = timeout

    async def fetch_forecast(self, latitude: float, longitude: float) -> OpenMeteoForecastResponse:
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": daily_params,
            "hourly": hourly_params,
            "current": current_params,
            "timezone": "auto",
            "timeformat": "unixtime",
        }
        response = await any_url_check.url_check(params, open_meteo_url, timeout=self._timeout)

        try:
            return OpenMeteoForecastResponse(**response)
        except Exception as exc:  
            raise ValueError(f"Invalid/Unexpected Open-Meteo response : {exc}") from exc

    async def save_weather(self, latitude: float, longitude: float, start_date : date, end_date: date, country: str, location_name: str) -> None:
        
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "weather_code,sunrise,sunset,daylight_duration,uv_index_max,"
                    "temperature_2m_max,apparent_temperature_max,wind_speed_10m_max,"
                    "wind_gusts_10m_max,wind_direction_10m_dominant,precipitation_probability_max",
            "timezone": "auto",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        response = await any_url_check.url_check(params, open_meteo_url, timeout=self._timeout)

        if "daily" not in response:
            raise HTTPException(status_code=502, detail="Invalid/Unexpected Open-Meteo response")

        forecast_by_day = transform_open_meteo_response(response)

        save = WeatherRequest(
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            country=country,
            location_name=location_name,
            forecast=forecast_by_day

        )
        try:
            save_weather(save)
        except Exception as exc:
            raise ValueError(f"Error saving weather data: {exc}") from exc
        return forecast_by_day



def transform_open_meteo_response(api_response: dict) -> list[dict]:
    """
    Transform the 'columnar' response from Open-Meteo into a list of objects 'by date'.
    Eg: {"time": ["d1","d2"], "temp": [20,21]} -> [{"date":"d1","temp":20}, {"date":"d2","temp":21}]
    """
    daily = api_response["daily"]
    dates = daily["time"]

    forecast_by_day = []
    for i, date in enumerate(dates):
        day_data = {
            "date": date,
            "weather_code": daily["weather_code"][i],
            "sunrise": daily["sunrise"][i],
            "sunset": daily["sunset"][i],
            "daylight_duration_s": daily["daylight_duration"][i],
            "uv_index_max": daily["uv_index_max"][i],
            "temperature_max_c": daily["temperature_2m_max"][i],
            "apparent_temperature_max_c": daily["apparent_temperature_max"][i],
            "wind_speed_max_kmh": daily["wind_speed_10m_max"][i],
            "wind_gusts_max_kmh": daily["wind_gusts_10m_max"][i],
            "wind_direction_dominant_deg": daily["wind_direction_10m_dominant"][i],
            "precipitation_probability_max_pct": daily["precipitation_probability_max"][i],
        }
        forecast_by_day.append(day_data)

    return forecast_by_day



open_meteo_service = OpenMeteoService()
