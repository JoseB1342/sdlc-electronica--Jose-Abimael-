from fastapi import FastAPI

from app.routers import alerts, reading_router, sensor_router

app = FastAPI(title="SensorHub API REST", version="1.0.0")

# Conectar los routers
app.include_router(alerts.router)
app.include_router(sensor_router.router)
app.include_router(reading_router.router)

@app.get("/")
def root() -> dict:
    return {"mensaje": "API funcionando correctamente"}

@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {"status": "ok", "message": "API de Alto Potencial funcionando correctamente"}