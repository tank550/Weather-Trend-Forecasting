"""
Service responsible solely for communicating with the Open-Meteo API
and parsing the response.
"""

import httpx
from model.weather_models import OpenMeteoForecastResponse
from service import any_url_check

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


        """try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(open_meteo_url, params=params)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ValueError(
                f"Open-Meteo has returned an error {exc.response.status_code}"
            ) from exc
        except httpx.RequestError as exc:
            raise ValueError(f"Unable to contact Open-Meteo : {exc}") from exc"""


        try:
            return OpenMeteoForecastResponse(**response)
        except Exception as exc:  
            raise ValueError(f"Invalid/Unexpected Open-Meteo response : {exc}") from exc


open_meteo_service = OpenMeteoService()
