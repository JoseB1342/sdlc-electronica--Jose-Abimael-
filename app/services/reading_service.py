from typing import Protocol
from datetime import datetime
from app.models.reading import ReadingModel

class ReadingRepository(Protocol):
    def add(self, sensor_id: str, value: float, unit: str) -> ReadingModel: ...
    def list_for_sensor(self, sensor_id: str, limit: int, offset: int, from_date: datetime | None, to_date: datetime | None) -> list[ReadingModel]: ...
    def get_by_id(self, reading_id: int) -> ReadingModel | None: ...
    def delete(self, reading_id: int) -> None: ...

class ReadingService:
    def __init__(self, repo: ReadingRepository) -> None:
        self._repo = repo

    def record(self, sensor_id: str, value: float, unit: str):
        if value < -273.15:
            # Esto detonará un Error 400 más adelante
            raise ValueError("Temperatura por debajo del cero absoluto")
        return self._repo.add(sensor_id, value, unit)

    def get_sensor_readings(self, sensor_id: str, limit: int, offset: int, from_date: datetime | None = None, to_date: datetime | None = None):
        return self._repo.list_for_sensor(sensor_id, limit, offset, from_date, to_date)
        
    def get_reading(self, reading_id: int):
        return self._repo.get_by_id(reading_id)
        
    def delete_reading(self, reading_id: int):
        self._repo.delete(reading_id)