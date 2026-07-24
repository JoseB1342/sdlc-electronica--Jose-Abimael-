from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: datetime = field(default_factory=datetime.now)

class AnomalyDetector:
    def __init__(self, max_temp: float, max_hum: float) -> None:
        self.max_temp = max_temp
        self.max_hum = max_hum

    def check(self, reading: SensorReading) -> tuple[bool, str | None]:
        if reading.temperature > self.max_temp:
            return True, "Temperatura Crítica"
        if reading.humidity > self.max_hum:
            return True, "Humedad Crítica"
        return False, None

#------------------------------------------------------------------

class AlertStrategy(Protocol):
    """Interfaz abstracta para todas las estrategias de alerta."""
    def send(self, sensor_id: str, message: str) -> None:
        ...

class ConsoleAlertStrategy:
    """Estrategia concreta 1: Imprime en la consola."""
    def send(self, sensor_id: str, message: str) -> None:
        print(f"[ALERTA] Sensor: {sensor_id} | Motivo: {message}")

class FileAlertStrategy:
    """Estrategia concreta 2: Guarda en un archivo .log"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def send(self, sensor_id: str, message: str) -> None:
        # "a" (append) añade texto sin borrar lo anterior
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"[ALERTA] Sensor: {sensor_id} | Motivo: {message}\n")

class AlertManager:
    """Orquestador que despacha alertas a múltiples estrategias."""
    def __init__(self, strategies: list[AlertStrategy]) -> None:
        self.strategies = strategies

    def dispatch(self, sensor_id: str, message: str) -> None:
        for strategy in self.strategies:
            strategy.send(sensor_id, message)