import pytest
from datetime import datetime
from semana2.eval1.iot import SensorReading

def test_sensor_reading_creation() -> None:
    # Given / When
    reading = SensorReading(sensor_id="SENS-01", temperature=25.0, humidity=50.0)
    
    # Then
    assert reading.sensor_id == "SENS-01"
    assert reading.temperature == 25.0
    assert reading.humidity == 50.0
    assert isinstance(reading.timestamp, datetime)