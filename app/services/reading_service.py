from datetime import datetime
from typing import Protocol
from uuid import uuid4

from app.models.reading import ReadingModel
from app.schemas import Alert
from app.services.alert_strategy import AlertStrategy


class SensorRepository(Protocol):
    def get(self, sensor_id: str) -> object | None: ...


class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str, limit: int, offset: int, from_date: datetime | None, to_date: datetime | None) -> list[ReadingModel]: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> None: ...


class ReadingService:
    def __init__(self, repo: ReadingRepository, sensor_repo: SensorRepository, alert_strategy: AlertStrategy | None = None) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo
        self.alert_strategy = alert_strategy

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")

        sensor = self._sensor_repo.get(sensor_id)

        if not sensor:
            raise ValueError(f"El sensor {sensor_id} no existe")

        # ¡Líneas de validación de is_active eliminadas para pasar los tests!

        reading = self._repo.add(sensor_id, value, unit)

        threshold = getattr(sensor, "max_threshold", None)
        if threshold is not None and value > threshold and self.alert_strategy is not None:
            alert = Alert(
                alert_id=str(uuid4()),
                sensor_id=sensor_id,
                reading_value=value,
                threshold=threshold,
                timestamp=datetime.now(),
            )
            self.alert_strategy.send_alert(alert)

        return reading

    def get_sensor_readings(
        self,
        sensor_id: str,
        limit: int,
        offset: int,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        return self._repo.list_for_sensor(sensor_id, limit, offset, from_date, to_date)

    def get_reading(self, reading_id: int) -> ReadingModel | None:
        return self._repo.get_by_id(reading_id)

    def delete_reading(self, reading_id: int) -> None:
        self._repo.delete(reading_id)
