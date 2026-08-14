from typing import Protocol

from sqlalchemy.orm import Session

from app.models.alert import AlertModel
from app.schemas import Alert


class AlertStrategy(Protocol):
    def send_alert(self, alert: Alert) -> None: ...


class LogAlertStrategy:
    def send_alert(self, alert: Alert) -> None:
        print(f"[ALERT] sensor_id={alert.sensor_id} alert_id={alert.alert_id} reading_value={alert.reading_value} threshold={alert.threshold} timestamp={alert.timestamp.isoformat()}")


class DBAlertStrategy:
    def __init__(self, db: Session) -> None:
        self.db = db

    def send_alert(self, alert: Alert) -> None:
        db_alert = AlertModel(
            alert_id=alert.alert_id,
            sensor_id=alert.sensor_id,
            reading_value=alert.reading_value,
            threshold=alert.threshold,
            timestamp=alert.timestamp,
        )
        self.db.add(db_alert)
        self.db.commit()
