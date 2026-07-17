import httpx
from model.geocoding import GeocodingResponse, Location


class GeocodingService:

    async def search_city(self, city: str) -> Location | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city}
            )

        response.raise_for_status()

        data = response.json()
        print(data)

        if not data.get("results"):
            return None

        return GeocodingResponse.model_validate(data)