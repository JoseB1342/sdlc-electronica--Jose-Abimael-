from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import engine, Base, SessionLocal

# 1. Importacion para que SQLite cree tablas
from app.models.sensor import SensorModel
from app.models.reading import ReadingModel

# 2. Fusibles pydantic
from app.schemas import SensorCreate, SensorOut, ReadingCreate, SensorReadingOut

# 3. Importamos los Repositorios (Drivers)
from app.repositories.sqlite_repo import SQLiteReadingRepository
from app.repositories.sqlite_repo import SQLiteSensorRepository 

# 4. Importamos los Servicios
from app.services.reading_service import ReadingService
from app.services.sensor_service import SensorService

app = FastAPI(title="SensorHub API REST", version="1.0.0")

# Esto lee los modelos y crea las tablas que falten en el disco duro
Base.metadata.create_all(bind=engine)

# --- INYECCIÓN DE DEPENDENCIAS ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reading_service(db: Session = Depends(get_db)):
    repo = SQLiteReadingRepository(db)
    return ReadingService(repo)

# NUEVO: Inyector para los sensores
def get_sensor_service(db: Session = Depends(get_db)):
    repo = SQLiteSensorRepository(db)
    return SensorService(repo)


# --- ENDPOINTS REST: SENSORES ---

# 1. Crear un Sensor (Evitando colisiones)
@app.post("/sensors", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: SensorCreate, service: SensorService = Depends(get_sensor_service)):
    try:
        return service.register_sensor(sensor.id, sensor.type, sensor.location)
    except ValueError as e:
        # 409 Conflict: El cliente intenta crear algo que ya existe (Ej. ID duplicado)
        raise HTTPException(status_code=409, detail=str(e))

# 2. Listar todos los Sensores
@app.get("/sensors", response_model=list[SensorOut])
def list_sensors(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: SensorService = Depends(get_sensor_service)
):
    return service.get_all_sensors(limit, offset)

# 3. Obtener un Sensor específico
@app.get("/sensors/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: str, service: SensorService = Depends(get_sensor_service)):
    sensor = service.get_sensor(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

# 4. Dar de baja un Sensor 
@app.delete("/sensors/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: str, service: SensorService = Depends(get_sensor_service)):
    try:
        service.remove_sensor(sensor_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return None


# --- ENDPOINTS REST: LECTURAS ---
@app.post("/sensors/{sensor_id}/readings", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def create_reading(sensor_id: str, reading: ReadingCreate, service: ReadingService = Depends(get_reading_service)):
    try:
        return service.record(sensor_id, reading.value, reading.unit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sensors/{sensor_id}/readings", response_model=list[SensorReadingOut])
def list_readings(
    sensor_id: str,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    service: ReadingService = Depends(get_reading_service)
):
    return service.get_sensor_readings(sensor_id, limit, offset, from_date, to_date)

@app.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(reading_id: int, service: ReadingService = Depends(get_reading_service)):
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    return reading

@app.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingService = Depends(get_reading_service)):
    reading = service.get_reading(reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Lectura no encontrada")
    service.delete_reading(reading_id)
    return None