from fastapi import FastAPI
from app.db import Base, engine
from app.routers import sensor_router, reading_router

app = FastAPI(title="SensorHub API REST", version="1.0.0")

# --- ZONA DE PELIGRO ---
# Comentado para proteger la base de datos en producción
# Base.metadata.drop_all(bind=engine) 
# -----------------------

# Crear tablas con el nuevo esquema
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