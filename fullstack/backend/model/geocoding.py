from pydantic import BaseModel

class Location(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    country: str
    country_code: str
    timezone: str
    postcodes: list[str] = []
    #city: str = None
    #province: str = None

class GeocodingResponse(BaseModel):
    results: list[Location] = []

