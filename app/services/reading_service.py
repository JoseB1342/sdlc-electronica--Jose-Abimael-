from datetime import datetime
from typing import Protocol
from uuid import uuid4

from app.models.reading import ReadingModel
from app.schemas import Alert
from app.services.alert_strategy import AlertStrategy


# 🔧 1. PROTOCOLOS UNIFICADOS
class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str, limit: int, offset: int, from_date: datetime | None, to_date: datetime | None) -> list[ReadingModel]: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> None: ...
    def get_statistics(self, sensor_id: str, from_date: datetime | None = None, to_date: datetime | None = None) -> dict: ...

class SensorRepository(Protocol):
    def get_by_id(self, sensor_id: str) -> object | None: ...

class AlertRepository(Protocol):
    def add(self, alert_id: str, sensor_id: str, reading_value: float, threshold: float, message: str, status: str) -> object: ...


class ReadingService:
    def __init__(
        self, 
        repo: ReadingRepository, 
        sensor_repo: SensorRepository, 
        alert_repo: AlertRepository | None = None,
        alert_strategy: AlertStrategy | None = None
    ) -> None:
        self._repo = repo
        self._sensor_repo = sensor_repo
        self._alert_repo = alert_repo
        self.alert_strategy = alert_strategy

    def record(self, sensor_id: str, value: float, unit: str) -> ReadingModel:
        if value < -273.15:
            raise ValueError("Temperatura por debajo del cero absoluto")

        # 🔧 2. LLAMADA DIRECTA AL REPOSITORIO
        sensor = self._sensor_repo.get_by_id(sensor_id)

        if not sensor:
            raise ValueError(f"El sensor {sensor_id} no existe")

        reading = self._repo.add(sensor_id, value, unit)

        threshold = getattr(sensor, "max_threshold", None)
        
        # --- INICIO DEL TEST POINT ---
        print("\n" + "="*30)
        print("🔧 DEBUG TIPO MULTÍMETRO 🔧")
        print(f"1. Valor de la lectura: {value}")
        print(f"2. Umbral (max_threshold): {threshold}")
        print(f"3. ¿Repo conectado?: {self._alert_repo is not None}")
        print("="*30 + "\n")
        # --- FIN DEL TEST POINT ---

        if threshold is not None and value > threshold:
            message = f"Anomalía detectada: Lectura ({value} {unit}) supera el límite máximo de {threshold} {unit}."
            alert_id = str(uuid4())
            
            if self.alert_strategy is not None:
                alert = Alert(
                    alert_id=alert_id,
                    sensor_id=sensor_id,
                    reading_value=value,
                    threshold=threshold,
                    message=message,   
                    status="open",     
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

    # 🔧 3. MÉTODO DE ESTADÍSTICAS AÑADIDO Y CORREGIDO
    def get_sensor_statistics(self, sensor_id: str, from_date: datetime | None = None, to_date: datetime | None = None) -> dict:
        sensor = self._sensor_repo.get_by_id(sensor_id)
        if not sensor:
            raise ValueError(f"El sensor {sensor_id} no existe")
            
        return self._repo.get_statistics(sensor_id, from_date, to_date)