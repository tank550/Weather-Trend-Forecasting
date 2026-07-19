from fastapi import APIRouter, HTTPException

from service.geocoding_service import geocoding_service

geocoding_router = APIRouter(
    prefix="/geocoding",
    tags=["geocoding"],
    responses={204: {"description": "No content"}},
)


@geocoding_router.get("/geocode")
async def geocode(address: str):
    try:
        return await geocoding_service.search_location(address)
    except ValueError as exc:
        raise HTTPException(status_code=204, detail=str(exc)) from exc