from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(tittle="SensorHub API", version="0.1.0")

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
def create_reading(reading: SensorReadingIn) -> SensorReadingOut:
    return SensorReadingOut(id=1, **reading.model.dump())