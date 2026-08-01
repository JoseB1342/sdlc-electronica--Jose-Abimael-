from typing import Protocol

from app.models.sensor import SensorModel


class SensorRepository(Protocol):
    def add(self,sensor_id: str, sensor_type: str, location:str) ->SensorModel:...
    def get_by_id(self, sensoir_id: str) -> SensorModel | None:...
    def list_all(self, limit: int, offset:int) -> list[SensorModel]:...
    def deactivate(self, sensor_id: str) -> bool:...

class SensorService:
    def __init__(self, repo: SensorRepository):
        self._repo = repo

    def register_sensor(self, sensor_id: str , sensor_type: str, location: str):
        existing = self._repo.get_by_id(sensor_id)
        if existing:
            raise ValueError(f"Conflicto: El sensor con ID {sensor_id} ya esta registrado")
        
        return self._repo.add(sensor_id, sensor_type, location)

    def get_sensor(self, sensor_id: str):
        return self._repo.get_by_id(sensor_id)

    def get_all_sensors(self, limit: int = 100, offset: int = 0):
        return self._repo.list_all(limit, offset)

    def remove_sensor(self, sensor_id: str):
        success = self._repo.deactivate(sensor_id)
        if not success:
            raise KeyError("Sensor no encontrado en la base de datos")