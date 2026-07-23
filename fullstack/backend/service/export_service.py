"""
Service responsible for exporting saved weather data (WeatherRequest records)
into several formats: JSON, CSV.
"""

import csv
import datetime
from http.client import HTTPException
import io
import json
from fastapi import responses

from db.model import WeatherRequest


def serialize_record(record: WeatherRequest) -> dict:
    """Convert a WeatherRequest ORM object into a JSON-serializable dict."""
    return {
        "id": str(record.id),
        "location_name": record.location_name,
        "country": record.country,
        "latitude": float(record.latitude) if record.latitude is not None else None,
        "longitude": float(record.longitude) if record.longitude is not None else None,
        "start_date": record.start_date.isoformat() if record.start_date else None,
        "end_date": record.end_date.isoformat() if record.end_date else None,
        "forecast": record.forecast or [],
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None,
    }


def to_dicts(records) -> list[dict]:
    """Normalize the input (single record, list of records, or None) into a list of dicts."""
    if records is None:
        return []
    if not isinstance(records, list):
        records = [records]
    return [serialize_record(r) for r in records]

def export_json(records) -> bytes:
    data = to_dicts(records)
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")

def export_csv(records) -> bytes:
    data = to_dicts(records)
    buffer = io.StringIO()
    fieldnames = [
        "id", "location_name", "country", "latitude", "longitude",
        "start_date", "end_date", "forecast", "created_at", "updated_at",
    ]
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        row = dict(row)
        row["forecast"] = json.dumps(row["forecast"], ensure_ascii=False)
        writer.writerow(row)
    return buffer.getvalue().encode("utf-8")


EXPORTERS = {
    "json": (export_json, "application/json", "json"),
    "csv": (export_csv, "text/csv", "csv"),
}

def export_response(data, format: str):
    if format not in EXPORTERS:
        raise HTTPException(status_code=400, detail="Unsupported format")

    export_func, media_type, ext = EXPORTERS[format]
    content = export_func(data)

    return responses.Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename=weather_export_{datetime.datetime.now().isoformat()}.{ext}"
        }
    )