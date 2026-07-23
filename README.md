# Weather Trend Forecasting — Backend

Backend API built with **FastAPI** for the Weather Trend Forecasting project. It serves weather data (current conditions, forecasts, history) by relying on the [Open-Meteo](https://open-meteo.com/) API, enriches forecasts using an LLM (via the NVIDIA NIM API), and persists user searches in a **PostgreSQL** database.

## Features

- 🌍 **Geocoding**: look up coordinates from a place name (Open-Meteo Geocoding API).
- ⛅ **Current weather**: temperature, humidity, wind, pressure, cloud cover, etc.
- 📅 **Forecasts & history**: save a date range (up to 16 days) to the database, with retrieval by ID, by location, or by date range.
- 🤖 **AI explanation**: an LLM (Nvidia Nemotron via NIM) turns raw weather data into human-readable recommendations (summary, clothing suggestions, activities, travel advice, health advice), returned as structured JSON.
- 🗄️ **PostgreSQL persistence** via SQLAlchemy (full CRUD on saved weather searches).

## Tech Stack

| Component        | Technology                        |
|-------------------|-------------------------------------|
| API Framework     | FastAPI + Uvicorn                   |
| Database          | PostgreSQL + SQLAlchemy (ORM)       |
| HTTP Client       | httpx (async)                       |
| Validation        | Pydantic                            |
| Generative AI     | OpenAI SDK → NVIDIA NIM (Nemotron)   |
| Weather Source    | Open-Meteo API (forecast + geocoding) |

## Project Structure

```
backend/
├── main.py                        # FastAPI entry point, router setup
├── prompt.md                      # System prompt used for AI explanation
├── requirements.txt
├── controller/                    # Route definitions (API layer)
│   ├── weather_controller.py
│   └── geocoding_controller.py
├── service/                       # Business logic
│   ├── weather_service.py         # Open-Meteo + LLM calls + DB orchestration
│   ├── geocoding_service.py       # Open-Meteo Geocoding calls
│   └── any_url_check.py           # Generic httpx wrapper with error handling
│   └── export_service.py          # Export to csv or json logics
├── model/                         # Pydantic schemas (DTO / request validation)
│   ├── weather_models.py
│   └── geocoding.py
└── db/                             # Database layer
    ├── database.py                # Connection, session, CRUD operations
    └── model.py                   # SQLAlchemy model (weather_requests table)
```

## Prerequisites

- Python 3.10+
- A reachable PostgreSQL database
- An NVIDIA NIM API key (for the AI weather-explanation endpoint)

## Installation

```bash
cd fullstack/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the root of the `backend/` folder with the following variables:

```env
# PostgreSQL connection
user=postgres_user
password=postgres_password
host=localhost
port=5432
dbname=weather_db

# NVIDIA NIM API key (LLM weather explanation)
nvidia_nim_api_key=your_nvidia_nim_api_key
```

## Running the App

```bash
uvicorn main:app --reload
```

The API is then available at `http://localhost:8000`, with interactive Swagger docs at `http://localhost:8000/docs` or directly in online (https://weather-trend-forecasting-3j9p.onrender.com/docs).

## Main Endpoints

### Health

| Method | Route        | Description                                        |
|--------|--------------|------------------------------------------------------|
| GET    | `/health/db` | Checks the database connection and creates tables if needed |

### Geocoding

| Method | Route                          | Description                                   |
|--------|----------------------------------|-------------------------------------------------|
| GET    | `/geocoding/geocode?address=`   | Looks up coordinates from a place name          |

### Weather

| Method | Route                                       | Description                                                        |
|--------|-----------------------------------------------|-----------------------------------------------------------------------|
| GET    | `/weather/current?lat=&lon=`                 | Current weather + hourly/daily forecast (Open-Meteo, not persisted)  |
| POST   | `/weather/save`                               | Fetches and saves a forecast for a date range (≤ 16 days)            |
| GET    | `/weather/all`                                | Lists all saved forecasts                                            |
| GET    | `/weather/location?lat=&lon=`                | Saved forecasts for a given location                                 |
| GET    | `/weather/date_range?start_date=&end_date=`  | Saved forecasts within a given date range                            |
| GET    | `/weather/{weather_id}`                      | Retrieves a saved forecast by its ID                                  |
| PATCH  | `/weather/{weather_id}`                      | Updates the date range of a saved forecast                           |
| DELETE | `/weather/{weather_id}`                      | Deletes a saved forecast                                              |
| POST   | `/weather/explain`                            | Sends a forecast to the LLM to get a structured explanation/recommendations (JSON) |

## Data Model (`weather_requests`)

| Field           | Type          | Description                        |
|------------------|---------------|---------------------------------------|
| `id`             | UUID          | Unique identifier                      |
| `location_name`  | String        | Location name                          |
| `country`        | String        | Country                                |
| `latitude`       | Numeric(9,6)  | Latitude                               |
| `longitude`      | Numeric(9,6)  | Longitude                              |
| `start_date`     | Date          | Start of the forecast range            |
| `end_date`       | Date          | End of the forecast range              |
| `forecast`       | JSONB         | Detailed daily forecast data           |
| `created_at`     | DateTime      | Creation timestamp                     |
| `updated_at`     | DateTime      | Last update timestamp                  |

## Notes

- The `/weather/current` and `/weather/save` endpoints query the Open-Meteo API in real time; any unavailability of that service returns a `502` error.
- The date range for `/weather/save` and its associated `PATCH` is limited to 16 days, in line with Open-Meteo's API limits.
- The `/weather/explain` endpoint follows a strict JSON schema (see `prompt.md`) covering summary, clothing advice, activities, travel advice, and health advice, with icons drawn from a predefined list.
