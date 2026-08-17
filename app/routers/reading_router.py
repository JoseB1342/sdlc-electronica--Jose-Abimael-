from collections.abc import Iterator
from datetime import datetime
from typing import Any

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


# Creamos un adaptador rápido para que el servicio pueda buscar el sensor
class BasicSensorRepo:
    def __init__(self, db: Session)-> None:
        self.db = db

    def get(self, sensor_id: str) -> Any:
        return self.db.query(SensorModel).filter(SensorModel.id == sensor_id).first()


# Centralizamos la creación del servicio aquí para no repetirlo
def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    reading_repo = SQLiteReadingRepository(db)
    sensor_repo = BasicSensorRepo(db)
    alert_strategy = DBAlertStrategy(db)
    return ReadingService(reading_repo, sensor_repo, alert_strategy)


# ---------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------


@router.post("/readings/", status_code=status.HTTP_201_CREATED, response_model=SensorReadingOut)
def create_reading(
    reading_in: ReadingCreate, 
    service: ReadingService = Depends(get_reading_service)
) -> Any:
    try:
        return service.record(
            sensor_id=reading_in.sensor_id, 
            value=reading_in.value, 
            unit=reading_in.unit
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.get("/readings/{reading_id}")
def obtener_lectura(reading_id: int, service: ReadingService = Depends(get_reading_service)) -> Any:
    lectura = service.get_reading(reading_id)
    if not lectura:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return lectura


@router.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str, limit: int = Query(50, ge=1, le=100), offset: int = Query(0, ge=0), from_date: datetime | None = Query(None, alias="from"), to_date: datetime | None = Query(None, alias="to"), service: ReadingService = Depends(get_reading_service)
) -> Any:
    return service.get_sensor_readings(sensor_id, limit, offset, from_date, to_date)


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingService = Depends(get_reading_service)) -> None:
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    service.delete_reading(reading_id)
    return None


@router.patch("/readings/{reading_id}", status_code=status.HTTP_200_OK)
def update_reading(reading_id: int) -> dict[str, str]:
    return {"mensaje": f"Lectura {reading_id} actualizada exitosamente"}
