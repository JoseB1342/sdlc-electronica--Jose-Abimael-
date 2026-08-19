from fastapi import APIRouter, Depends, HTTPException

from app.db import SessionLocal
from app.repositories.alert import SQLAlchemyAlertRepository
from app.schemas import AlertResponse, AlertStatusUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# Inyección de dependencias
def get_alert_service():
    db = SessionLocal()
    try:
        repo = SQLAlchemyAlertRepository(db)
        yield AlertService(repo)
    finally:
        db.close()

@router.get("/active", response_model=list[AlertResponse])
def get_active_alerts(service: AlertService = Depends(get_alert_service)):
    """Consulta todas las alertas que están en estado 'open'"""
    return service.get_active_alerts()

@router.patch("/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(alert_id: str, update_data: AlertStatusUpdate, service: AlertService = Depends(get_alert_service)):
    """Cambia el estado de una alerta (ej. de open a acknowledged o resolved)"""
    try:
        return service.change_alert_status(alert_id, update_data.status)
    except ValueError as e:
        # Transformamos el error de negocio en un error HTTP
        status_code = 404 if "no encontrada" in str(e) else 400
        raise HTTPException(status_code=status_code, detail=str(e)) from e