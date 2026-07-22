class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def __init__(self) -> None:
        self._sensors: dict[str, str] = {}

    def _validate_exists(self, sensor_id: str) -> None:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor {sensor_id} no encontrado.")

    def get(self, sensor_id: str):
        self._validate_exists(sensor_id)
        return self._sensors[sensor_id]