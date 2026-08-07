from fastapi import FastAPI
from app.db import Base, engine
from app.routers import sensor_router, reading_router

app = FastAPI(title="SensorHub API REST", version="1.0.0")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Conectar los routers
app.include_router(sensor_router.router)
app.include_router(reading_router.router)

@app.get("/")
def root() -> dict:
    return {"mensaje": "API funcionando correctamente"}

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}