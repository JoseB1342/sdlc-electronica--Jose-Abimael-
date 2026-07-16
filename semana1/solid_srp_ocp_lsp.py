from abc import ABC, abstractmethod

class SensorReading:
    def __init__(self, sensor_id: str, value: float, timestamp: str):
        self.sensor_id = sensor_id
        self.value = value
        self.timestamp = timestamp

"""esta parte esta mal ya que una sola clase esta haciendo dos cosas, leer el sensor y guardar la lectura, lo cual viola el principio de responsabilidad unica"""
class ViolacionSRP:
    def __init__(self) -> None: 
        self.hitorial_guardado = []
    
    def guardar_lectura(self, sensor_id: str, value: float, timestamp: str) -> None:
        lectura = SensorReading(sensor_id, value, timestamp)
        self.hitorial_guardado.append(lectura)


"""Esta esta bien ya que las clases estan separadas y cada una tiene sus responsabilidad, una leer y la otra guardar la lectura, cumpliendo con el principio de responsabilidad unica"""
class SensorReader:
    def Read_sensor(self, sensor_id: str, value: float, timestamp: str) -> SensorReading:
        # Lógica para leer el sensor y obtener el valor y la marca de tiempo
        lectura = SensorReading(sensor_id, value, timestamp)
        return lectura
    
class DataLogger:
    def __init__(self) -> None:
        self.hitorial_guardado = []
        
    def guardar_lectura(self, sensor_id: str, value: float, timestamp: str) -> None:
        lectura = SensorReading(sensor_id, value, timestamp)
        self.hitorial_guardado.append(lectura)

"""///////////////////////////////////////////////////////////////////////////////////////////////////"""
class ViolationOCP:
    def __init__(self, tipo_alerta: str) -> None:
        self.tipo_alerta = tipo_alerta

    def verificar_y_enviar(self, reading: SensorReading, threshold: float) -> None:
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
    def send_alert(self, reading: SensorReading, threshold: float) -> None:
        pass

class ConsoleAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> None:
        if reading.value > threshold:
            return(f"[console] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}")

class FileAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> None:
        if reading.value > threshold:
            with open("alertas.txt", "a") as file:
                file.write(f"[file] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}\n")

class EmailAlertSender(AlertSender):
    def send_alert(self, reading: SensorReading, threshold: float) -> None:
        if reading.value > threshold:
            # Lógica para enviar un correo electrónico
            return(f"[email] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}")

class AnomalyDetector:
    def __init__(self, alert_sender: AlertSender) -> None:
        self.alert_sender = alert_sender

    def detectar_anomalia(self, reading: SensorReading, threshold: float) -> None:
        if reading.value > threshold:
            self.alert_sender.send_alert(reading, threshold)
            return f"[{self.alert_sender.__class__.__name__.replace('AlertSender', '').lower()}] Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        

    def check(self, reading: SensorReading, threshold: float) -> str:
        if reading.value > threshold:
            return f"Alerta: El valor del sensor {reading.sensor_id} excede el umbral de {threshold}. Valor actual: {reading.value}"
        return "Normal"
    
"""Principio 3 Liskov Substitution Principle (LSP)"""

class BaseSensorMal:
    def get_reading(self) ->float:
        return 0.0
    
class TemperatureSensorMal(BaseSensorMal):
    def get_reading(self) ->float:
        return 25.0
    
class HumiditySensorMal(BaseSensorMal):
    def get_reading(self) ->float:
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