import pytest
from datetime import datetime
from semana2.eval1.iot import SensorReading
from semana2.eval1.iot import SensorReading, AnomalyDetector
def test_sensor_reading_creation() -> None:
    reading = SensorReading(sensor_id="SENS-01", temperature=25.0, humidity=50.0)
    
    assert reading.sensor_id == "SENS-01"
    assert reading.temperature == 25.0
    assert reading.humidity == 50.0
    assert isinstance(reading.timestamp, datetime)

def test_anomaly_detector_injected_thresholds() -> None:
    detector = AnomalyDetector(max_temp=35.0, max_hum=80.0)

    normal_reading = SensorReading("S-1", 25.0, 50.0)
    hot_reading = SensorReading("S-2", 36.0, 50.0)
    humid_reading = SensorReading("S-3", 25.0, 85.0)
    
    assert detector.check(normal_reading) == (False, None)
    assert detector.check(hot_reading) == (True, "Temperatura Crítica")
    assert detector.check(humid_reading) == (True, "Humedad Crítica")