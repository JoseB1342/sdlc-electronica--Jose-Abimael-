from typing import Any
from typing import Protocol

from app.models.alert import AlertModel


# Contrato para el repositorio
class AlertRepository(Protocol):
    def get_all_active(self) -> list[AlertModel]: ...
    def update_status(self, alert_id: str, new_status: str) -> AlertModel | None: ...

class AlertService:
    def __init__(self, repo: AlertRepository):
        self._repo = repo

    def get_active_alerts(self) -> Any:
        return self._repo.get_all_active()

    def change_alert_status(self, alert_id: str, new_status: str) -> Any:
        # Validación de negocio
        valid_statuses = ["open", "acknowledged", "resolved"]
        if new_status not in valid_statuses:
            raise ValueError(f"Estado no válido. Use: {', '.join(valid_statuses)}")
            
        alert = self._repo.update_status(alert_id, new_status)
        
        if not alert:
            raise ValueError("Alerta no encontrada")
            
        return alert