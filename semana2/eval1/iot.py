from dataclasses import dataclass, field
from datetime import datetime

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