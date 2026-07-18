from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class SensorReading:
    def __init__(self, sensor_id: str, value: float, timestamp: str):
        self.sensor_id = sensor_id
        self.value = value
        self.timestamp = timestamp

"""esta parte esta mal ya que una sola clase esta haciendo dos cosas, leer el sensor y guardar la lectura, lo cual viola el principio de responsabilidad unica"""
class ViolacionSRP:
    def __init__(self) -> None: 
        # CORRECCIÓN: Se declara como atributo de instancia usando 'self.' y se corrige el dedazo 'hitorial'
        self.historial_guardado: list[SensorReading] = []
    
    def guardar_lectura(self, sensor_id: str, value: float, timestamp: str) -> None:
        lectura = SensorReading(sensor_id, value, timestamp)
        # CORRECCIÓN: Se usa el atributo de instancia correcto de forma operativa
        self.historial_guardado.append(lectura)

"""Esta esta bien ya que las clases estan separadas y cada una tiene sus responsabilidad, una leer y la otra guardar la lectura, cumpliendo con el principio de responsabilidad unica"""
class SensorReader:
    def Read_sensor(self, sensor_id: str, value: float, timestamp: str) -> SensorReading:
        lectura = SensorReading(sensor_id, value, timestamp)
        return lectura
    
class DataLogger:
    def __init__(self) -> None:
        # CORRECCIÓN: Consistencia en el nombre del atributo corregido sin dedazos
        self.historial_guardado: list[SensorReading] = []
        
    def guardar_lectura(self, sensor_id: str, value: float, timestamp: str) -> None:
        lectura = SensorReading(sensor_id, value, timestamp)
        self.historial_guardado.append(lectura)

"""Principio 2 Open/Closed Principle (OCP)"""
class ViolationOCP:
    def __init__(self, tipo_alerta: str) -> None:
        self.tipo_alerta = tipo_alerta

    # CORRECCIÓN: La firma decía '-> None' pero tiene sentencias 'return string'. Se cambia a '-> str'
    def verificar_y_enviar(self, reading: SensorReading, threshold: float) -> str:
        if reading.value > threshold:
            if self.tipo_alerta == "console":
                return f"[console] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
            elif self.tipo_alerta == "email":
                return f"[email] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
            elif self.tipo_alerta =="file":
                return f"[file] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        return "Normal"
    
class AlertSender(ABC):
    @abstractmethod
    # CORRECCIÓN: Estandarización del tipo de 'threshold' a float y retorno '-> Optional[str]' 
    # debido a que las alertas solo devuelven texto si se cruza el umbral
    def send_alert(self, reading: SensorReading, threshold: float) -> Optional[str]:
        pass

class ConsoleAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> Optional[str]:
        if reading.value > threshold:
            return f"[console] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        # CORRECCIÓN: Si no entra al if, debe retornar explícitamente un valor para no violar la firma de tipos
        return None

class FileAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> Optional[str]:
        if reading.value > threshold:
            with open("alertas.txt", "a") as file:
                file.write(f"[file] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}\n")
            return f"[file] Alerta escrita en disco"
        return None

class EmailAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> Optional[str]:
        if reading.value > threshold:
            return f"[email] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        return None

class AnomalyDetector:
    def __init__(self, alert_sender: AlertSender) -> None:
        self.alert_sender = alert_sender

    # CORRECCIÓN: La firma declaraba '-> None' pero tiene un return de texto interno. Se cambia a '-> Optional[str]'
    def detectar_anomalia(self, reading: SensorReading, threshold: float) -> Optional[str]:
        if reading.value > threshold:
            self.alert_sender.send_alert(reading, threshold)
            return f"[{self.alert_sender.__class__.__name__.replace('AlertSender', '').lower()}] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        return None
        
    def check(self, reading: SensorReading, threshold: float) -> str:
        if reading.value > threshold:
            return f"Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        return "Normal"
    
"""Principio 3 Liskov Substitution Principle (LSP)"""
class BaseSensorMal:
    def get_reading(self) -> float:
        return 0.0
    
class TemperatureSensorMal(BaseSensorMal):
    def get_reading(self) -> float:
        return 25.0
    
class HumiditySensorMal(BaseSensorMal):
    def get_reading(self) -> float:
        raise ValueError("No se puede obtener la lectura de humedad de un sensor de temperatura")
    
class BaseSensor(ABC):
    @abstractmethod
    def get_reading(self) -> float:
        pass

class TemperatureSensor(BaseSensor):
    def get_reading(self) -> float:
        return 25.0
    
class HumiditySensor(BaseSensor):
    def get_reading(self) -> float:
        return 60.0
    
def process_sensor(sensor: BaseSensor) -> float:
    return sensor.get_reading()