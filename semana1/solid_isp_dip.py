from typing import Protocol, List, Optional
from abc import ABC, abstractmethod

class SensorRecording:
    def __init__ (self, Sensor_id:str, value: float, Timestamp: str) -> None:
        self.sensor_id = Sensor_id
        self.value = value
        self.timestamp = Timestamp

class InterfazSensorGorda(ABC):
    @abstractmethod
    def read(self) -> float: pass

    @abstractmethod
    def write(self, value: float) ->None:pass

    @abstractmethod
    def calibrate(self) -> str:pass

    @abstractmethod
    def reset (self) ->None:pass

class SensorBasicoTemperaturaMal(InterfazSensorGorda):
    def read(self) ->float:
        return 23.4
    
    def write (self, value:float) -> None:
        raise NotImplementedError("Este sensor no soporta escritura")
    
    def calibrate(self) -> str:
        raise NotImplementedError("No calibrado")
    
    def reset(self) -> None:
        pass

"""Parte bien"""

class Readable(Protocol):
    def read(self) -> float:...

class Writable(Protocol):
    def write(self,value:float) -> None:...
    
class Calibratable(Protocol):
    def calibrate(self) -> str:...

class SensorBasicoTemperatura(Readable):
    def read(self) -> float:
        return 23.4
    
class SensorInteligenteIndustrial(Readable, Writable, Calibratable):
    def __init__(self) -> None:
        self.valor_interno = 0.0
    
    def read (self) -> float:
        return self.valor_interno
    
    def write(self, value) -> None:
        self.valor_interno = value
    
    def calibrate(self) ->str:
        return ("Calibracion exitosa")
    
"""////////////////////////////////Principio D////////////////////"""
class SQLServerRepository:
    def save_to_sql(self, reading: SensorRecording) -> None:
        pass

class DataProcessMal:
    def __init__(self) -> None:
        self._repo = SQLServerRepository()

    def procesar(self,reading :SensorRecording) ->None:
        self._repo.save_to_sql(reading)

"""Prinicpio D Bien"""
class DataRepository(Protocol):
    def save(self, reading: SensorRecording) -> None:...
    def get_latest(self,sensor_id: str) -> Optional[SensorRecording]:...

class DataProcessor:
    def __init__(self, repository: SensorRecording) -> None:
        self._repo = repository
    
    def procesar(self, reading: SensorRecording) ->None:
        self._repo.save(reading)

    def obtener_ultimo(self, sensor_id: str) -> Optional[SensorRecording]:
        return self._repo.get_latest(sensor_id)
    
class InMemoryRepository(DataRepository):
    def __init__(self) -> None:
        self.storage : List[SensorRecording] = []

    def save(self,reading: SensorRecording) -> None:
        self.storage.append(reading)

    def get_latest(self, sensor_id: str,) -> Optional[SensorRecording]:
        for r in reversed(self.storage):
            if  r.sensor_id == sensor_id:
                return r 
            return None