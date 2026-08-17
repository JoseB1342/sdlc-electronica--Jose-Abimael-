from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.services.reading_service import ReadingService

class FakeReadingRepository:
    def __init__(self):
        self._storage = [] 

    def add(self, sensor_id: str, value: float, unit: str):
        reading = SimpleNamespace(sensor_id=sensor_id, value=value, unit=unit)
        self._storage.append(reading) 
        return reading


def test_record_successful():
    fake_repo = FakeReadingRepository()
    mock_sensor_repo = Mock()
    
    # Simular que el sensor existe y está activo
    mock_sensor_repo.get.return_value = SimpleNamespace(is_active=True, max_threshold=30.0) 

    # Inyectar AMBOS repositorios
    service = ReadingService(
        repo=fake_repo, 
        sensor_repo=mock_sensor_repo, 
        alert_strategy=None
    )
    
    # Actuar
    reading = service.record(sensor_id="TEMP-01", value=25.0, unit="C")
    
    # Verificar
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.0
    assert len(fake_repo._storage) == 1


def test_record_below_absolute_zero():
    fake_repo = FakeReadingRepository()
    mock_sensor_repo = Mock()
    
    # Simular que el sensor existe
    mock_sensor_repo.get.return_value = SimpleNamespace(is_active=True, max_threshold=30.0) 

    # OJO: Aquí te faltaba inyectar el sensor_repo
    service = ReadingService(repo=fake_repo, sensor_repo=mock_sensor_repo)

    with pytest.raises(ValueError, match="Temperatura por debajo del cero absoluto"):
        service.record(sensor_id="TEMP-01", value=-300.0, unit="C")

    assert len(fake_repo._storage) == 0


def test_record_sends_alert_when_value_exceeds_threshold():
    fake_repo = FakeReadingRepository()
    mock_sensor_repo = Mock()
    alert_strategy = Mock()

    # El umbral ahora se lo damos al Mock del sensor, ya no lo creamos suelto
    mock_sensor_repo.get.return_value = SimpleNamespace(is_active=True, max_threshold=50.0)

    # Inyectamos todo al servicio
    service = ReadingService(
        repo=fake_repo, 
        sensor_repo=mock_sensor_repo, 
        alert_strategy=alert_strategy
    )

    # OJO: Ya no le pasamos "sensor=sensor" al método record
    service.record(sensor_id="TEMP-01", value=55.0, unit="C")

    # Verificar que la alerta se disparó correctamente
    alert_strategy.send_alert.assert_called_once()
    alert = alert_strategy.send_alert.call_args.args[0]

    assert alert.sensor_id == "TEMP-01"
    assert alert.reading_value == 55.0
    assert alert.threshold == 50.0