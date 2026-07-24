from datetime import datetime
from pathlib import Path
from typing import Any

from semana2.eval1.iot import (
    AlertManager,
    AnomalyDetector,
    ConsoleAlertStrategy,
    FileAlertStrategy,
    SensorReading,
)


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

#-----------------------------------------------------------

def test_alert_manager_console(capsys: Any) -> None:
    strategy = ConsoleAlertStrategy()
    manager = AlertManager(strategies=[strategy])
    
    manager.dispatch("SENS-99", "Temperatura Crítica")
    
    captured = capsys.readouterr()
    assert "SENS-99" in captured.out
    assert "Temperatura Crítica" in captured.out

def test_alert_manager_file(tmp_path: Path) -> None:
    log_file = tmp_path / "test_alerts.log"
    strategy = FileAlertStrategy(filepath=str(log_file))
    manager = AlertManager(strategies=[strategy])
    
    manager.dispatch("SENS-88", "Humedad Crítica")
    
    content = log_file.read_text()
    assert "SENS-88" in content
    assert "Humedad Crítica" in content