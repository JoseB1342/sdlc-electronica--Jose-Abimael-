from typing import Any
from sqlalchemy.orm import Session

from app.models.alert import AlertModel


class SQLAlchemyAlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, alert_id: str, sensor_id: str, reading_value: float, threshold: float, message: str, status: str) -> Any:
        nueva_alerta = AlertModel(
            alert_id=alert_id,
            sensor_id=sensor_id,
            reading_value=reading_value,
            threshold=threshold,
            message=message,
            status=status
        )
        self.db.add(nueva_alerta)
        self.db.commit()
        self.db.refresh(nueva_alerta)
        return nueva_alerta
        
    def get_all_active(self) -> list[AlertModel]:
        """Útil para el RF-5: Consultar alertas activas"""
        return self.db.query(AlertModel).filter(AlertModel.status == "open").all()
        
    def update_status(self, alert_id: str, new_status: str) -> AlertModel | None:
        """Útil para el RF-5: Cambiar estado (open/acknowledged/resolved)"""
        alert = self.db.query(AlertModel).filter(AlertModel.alert_id == alert_id).first()
        if alert:
            alert.status = new_status
            self.db.commit()
            self.db.refresh(alert)
        return alert