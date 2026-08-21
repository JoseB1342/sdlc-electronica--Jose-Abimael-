from fastapi import FastAPI

from app.mqtt_client import start_mqtt_client
from app.routers import alerts, reading_router, sensor_router

app = FastAPI(title="SensorHub API REST", version="1.0.0")

@app.on_event("startup")
async def startup_event() -> None:
    start_mqtt_client()
    
# Conectar los routers
app.include_router(alerts.router)
app.include_router(sensor_router.router)
app.include_router(reading_router.router)

@app.get("/")
def root() -> dict:
    return {"mensaje": "API funcionando correctamente"}

@app.get("/health", tags=["Monitoreo"])
def health_check() -> dict:
    return {"status": "ok", "message": "API de Alto Potencial funcionando correctamente"}