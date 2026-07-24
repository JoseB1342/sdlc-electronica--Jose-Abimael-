from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class SensorReading:
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: datetime = field(default_factory=datetime.now)