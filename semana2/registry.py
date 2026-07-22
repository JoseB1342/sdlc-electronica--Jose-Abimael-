class SensorNotFoundError(Exception):
    pass

class SensorRegistry:
    def __init__(self)-> None:
        self._sensors = {}
    
    def get (self, sensor_id: str):
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"Sensor{sensor_id}no encontrado.")
        return self._sensors[sensor_id]