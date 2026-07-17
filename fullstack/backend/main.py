from fastapi import FastAPI
from controller.geocoding_controller import geocoding_router

app = FastAPI()


app.include_router(geocoding_router)