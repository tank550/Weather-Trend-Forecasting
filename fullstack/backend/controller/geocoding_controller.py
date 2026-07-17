from fastapi import APIRouter

from service.requestvalidate import GeocodingService

geocoding_router = APIRouter()
service = GeocodingService()

@geocoding_router.get("/geocode")
async def geocode(address: str):
    return await service.geocode(address)