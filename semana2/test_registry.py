import pytest 
from semana2.registry import SensorNotFoundError, SensorRegistry
def test_get_unknown_sensor_raises():
    registry = SensorRegistry()
    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")