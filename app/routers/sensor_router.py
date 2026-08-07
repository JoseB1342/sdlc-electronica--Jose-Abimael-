from typing import Iterator, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.repositories.sqlite_repo import SQLiteSensorRepository
from app.schemas import SensorCreate, SensorOut
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["sensors"])

# Inyector local de base de datos
def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    repo = SQLiteSensorRepository(db)
    return SensorService(repo)

@router.post("", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorCreate, service: SensorService = Depends(get_sensor_service)) -> Any:
    try:
        return service.register_sensor(sensor.id, sensor.type, sensor.location)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e

@router.get("", response_model=list[SensorOut])
def list_sensors(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: SensorService = Depends(get_sensor_service)
) -> Any:
    return service.get_all_sensors(limit, offset)

@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: str, service: SensorService = Depends(get_sensor_service)) -> Any:
    sensor = service.get_sensor(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: str, service: SensorService = Depends(get_sensor_service)) -> None:
    try:
        service.remove_sensor(sensor_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail="Sensor no encontrado") from e
    return None