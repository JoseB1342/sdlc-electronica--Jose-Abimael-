from typing import Protocol

from app.models.sensor import SensorModel


class SensorRepository(Protocol):
    def add(self, sensor_id: str, sensor_type: str, location: str) -> SensorModel: ...
    def get_by_id(self, sensoir_id: str) -> SensorModel | None: ...
    def list_all(self, limit: int, offset: int) -> list[SensorModel]: ...
    def deactivate(self, sensor_id: str) -> bool: ...


class SensorService:
    def __init__(self, repo: SensorRepository) -> None:
        self._repo = repo

    def register_sensor(self, sensor_id: str, sensor_type: str, location: str) -> SensorModel:
        # NUEVO: Validar que los textos no estén vacíos
        if not sensor_id.strip() or not sensor_type.strip() or not location.strip():
            raise ValueError("Error: El ID, tipo y ubicación del sensor no pueden estar vacíos.")

        existing = self._repo.get_by_id(sensor_id)
        if existing:
            raise ValueError(f"Conflicto: El sensor con ID {sensor_id} ya esta registrado")

        return self._repo.add(sensor_id, sensor_type, location)

    def get_sensor(self, sensor_id: str) -> SensorModel | None:
        return self._repo.get_by_id(sensor_id)

    def get_all_sensors(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:
        # NUEVO: Proteger contra denegación de servicio (DoS) y números negativos
        if limit <= 0 or limit > 500:
            raise ValueError("Error: El límite debe estar entre 1 y 500.")
        if offset < 0:
            raise ValueError("Error: El offset no puede ser negativo.")

        return self._repo.list_all(limit, offset)

    def remove_sensor(self, sensor_id: str) -> None:
        success = self._repo.deactivate(sensor_id)
        if not success:
            raise ValueError("Sensor no encontrado") 