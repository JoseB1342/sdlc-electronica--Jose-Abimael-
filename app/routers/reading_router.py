from typing import Any, Iterator
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models.sensor import SensorModel
from app.repositories.sqlite_repo import SQLiteReadingRepository
from app.schemas import ReadingCreate, SensorReadingOut
from app.services.alert_strategy import DBAlertStrategy
from app.services.reading_service import ReadingService

router = APIRouter(tags=["readings"])

def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    repo = SQLiteReadingRepository(db)
    return ReadingService(repo, DBAlertStrategy(db))

@router.post("/sensors/{sensor_id}/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def create_reading(sensor_id: str, reading: ReadingCreate, service: ReadingService = Depends(get_reading_service), db: Session = Depends(get_db)) -> Any:
    try:
        sensor = db.get(SensorModel, sensor_id)
        return service.record(sensor_id, reading.value, reading.unit, sensor=sensor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    service: ReadingService = Depends(get_reading_service)
) -> Any:
    return service.get_sensor_readings(sensor_id, limit, offset, from_date, to_date)

@router.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, service: ReadingService = Depends(get_reading_service)) -> Any:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading

@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingService = Depends(get_reading_service)) -> None:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    service.delete_reading(reading_id)
    return None

# El PATCH sugerido por tu compañero para actualizar parcialmente
@router.patch("/readings/{reading_id}", status_code=status.HTTP_200_OK)
def update_reading(reading_id: int) -> dict[str, str]:
    # Nota: Aquí después implementarás la lógica con la base de datos
    return {"mensaje": f"Lectura {reading_id} actualizada exitosamente"}