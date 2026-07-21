from fastapi import HTTPException
import httpx
from model.geocoding import GeocodingResponse, Location
from service.any_url_check import url_check


geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

class GeocodingService:

    ## Service responsible solely for communicating with the Open-Meteo Geocoding API
    ## and parsing the response.
    async def search_location(self, address: str):
        """async with httpx.AsyncClient() as client:
            response = await client.get(
                geocoding_url,
                params={"name": address}
            )"""

        params = {"name": address}
        url_check_response = await url_check(params, geocoding_url)

        data = url_check_response

        # Check if the response contains results
        if not data.get("results"):
            raise ValueError("No results found for the given address.")
    
        return GeocodingResponse.model_validate(data)
    

geocoding_service = GeocodingService()