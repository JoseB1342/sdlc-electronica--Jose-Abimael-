from fastapi import FastAPI, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import engine, Base, SessionLocal
from app.models.reading import ReadingModel
from app.services.reading_service import ReadingService
from app.repositories.sqlite_repo import SQLiteReadingRepository

app = FastAPI(title="SensorHub API REST", version="0.2.0")
Base.metadata.create_all(bind=engine)

# ---------------------
class ReadingCreate(BaseModel):
    value: float
    unit: str = "C"

class SensorReadingOut(ReadingCreate):
    id: int
    sensor_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ---------------------------- ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_reading_service(db: Session = Depends(get_db)):
    repo = SQLiteReadingRepository(db)
    return ReadingService(repo)

# -------------------------------

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