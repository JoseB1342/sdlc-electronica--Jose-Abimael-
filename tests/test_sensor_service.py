import pytest
from unittest.mock import Mock

# Ajusta estas importaciones a la ruta real de tus archivos
# from app.models.sensor import SensorModel
# from app.services.sensor_service import SensorService

@pytest.fixture
def repo_mock():
    return Mock()

@pytest.fixture
def sensor_service(repo_mock):
    # ¡Esta es la ruta real que vimos en tu imagen!
    from app.services.sensor_service import SensorService 
    return SensorService(repo_mock)

# Test 1: Límite máximo (Seguridad)
def test_get_all_sensors_limite_excedido(sensor_service):
    with pytest.raises(ValueError, match="El límite debe estar entre 1 y 500"):
        sensor_service.get_all_sensors(limit=9999)

# Test 2: Paginación negativa (Caso Borde)
def test_get_all_sensors_offset_negativo(sensor_service):
    with pytest.raises(ValueError, match="El offset no puede ser negativo"):
        sensor_service.get_all_sensors(limit=10, offset=-5)

# Test 3: Registro con strings vacíos (Integridad)
def test_register_sensor_datos_vacios(sensor_service):
    with pytest.raises(ValueError, match="no pueden estar vacíos"):
        sensor_service.register_sensor(sensor_id="   ", sensor_type="RS-485", location="Xalapa")

# Test 4: Sensor duplicado (Lógica de Negocio)
def test_register_sensor_duplicado(sensor_service, repo_mock):
    # Simulamos que la base de datos ya tiene un sensor con ese ID
    repo_mock.get_by_id.return_value = Mock() 
    
    with pytest.raises(ValueError, match="ya esta registrado"):
        sensor_service.register_sensor(sensor_id="ESP32-A1", sensor_type="TMP", location="Lab")

# Test 5: Desactivar sensor inexistente (Manejo de Errores)
def test_remove_sensor_inexistente(sensor_service, repo_mock):
    # Simulamos que la base de datos devuelve False al intentar borrar
    repo_mock.deactivate.return_value = False
    
    with pytest.raises(ValueError, match="Sensor no encontrado"):
        sensor_service.remove_sensor(sensor_id="I2C-GHOST")