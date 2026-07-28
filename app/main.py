from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.db import engine, Base, SesionLocal
from app.models.reading import ReadingModel

app = FastAPI(tittle="SensorHub API", version="0.1.0")
Base.metadata.create_all(bind=engine)

def get_db():
    db = SesionLocal()
    try: 
        yield db 
    finally:
        db.close()

    
class SensorReadingIn(BaseModel):
    sensor_id: str  = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

class SensorReadingOut(SensorReadingIn):
    id: int

@app.get("/health")
def healt()-> dict[str,str]:
    return {"status": "ok"}

@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(reading: SensorReadingIn, db: Session = Depends(get_db)) -> SensorReadingOut:
    db_reading = ReadingModel(
        sensor_id=reading.sensor_id,
        value = reading.value,
        unit = reading.unit
    )
    db.add(db_reading)

    db.commit()

    db.refresh(db_reading)

    return db_reading