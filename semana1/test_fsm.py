import pytest
# Aquí le decimos a Python que vaya a tu archivo fsm_demo y traiga el semáforo
from semana1.fsm_demo import TrafficLightFSM, TrafficLightState
from semana1.solid_srp_ocp_lsp import AnomalyDetector, ConsoleAlertSender, EmailAlertSender, SensorReading, ViolationOCP
from semana1.solid_srp_ocp_lsp import (
    TemperatureSensorMal, HumiditySensorMal, 
    TemperatureSensor, HumiditySensor
)
from semana1.solid_isp_dip import SensorBasicoTemperaturaMal, SensorBasicoTemperatura, SensorInteligenteIndustrial
from semana1.solid_isp_dip import DataProcessMal, DataProcessor, InMemoryRepository


def test_initial_state():
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED

def test_transition_red_to_green():
    fsm = TrafficLightFSM()
    fsm.transition()
    assert fsm.state == TrafficLightState.GREEN

def test_full_cycle_returns_to_red():
    fsm = TrafficLightFSM()
    # Damos la vuelta completa
    fsm.transition()  # Pasa a GREEN
    fsm.transition()  # Pasa a YELLOW
    fsm.transition()  # Pasa a RED
    
    # Comprobamos que regresó al inicio
    assert fsm.state == TrafficLightState.RED

def test_cycle_counter_increments():
    fsm = TrafficLightFSM()
    fsm.transition()  # Primer transición
    fsm.transition()  # Segunda transición
    
    # Comprobamos que el contador interno es 2
    assert fsm._cycle_count == 2

"""///////////////////////////////////////// Principio 2 OPEN/CLOSE ///////////////////////////////////////////"""
def test_ocp_vilation():
    detector_mal = ViolationOCP("console")
    lectura = SensorReading("Temp_01", 35.0, "2024-06-01T12:00:00Z")
    resultado = detector_mal.verificar_y_enviar(lectura, 30.0)
    assert resultado == "[console] Alerta: El valor del sensor Temp_01 excede el umbral de 30.0. Valor actual: 35.0"

def test_ocp_corrrecto():
    lectura = SensorReading("Temp_01", 35.0, "2024-06-01T12:00:00Z")
    
    # 1. Cambiamos [consola] por [console] para que cuadre con tu clase
    detector_consola = AnomalyDetector(ConsoleAlertSender())
    assert detector_consola.detectar_anomalia(lectura, 30.0) == "[console] Alerta: El valor del sensor Temp_01 excede el umbral de 30.0. Valor actual: 35.0"

    # 2. Cambiamos [correo] por [email] para que cuadre con tu clase EmailAlertSender
    detector_email = AnomalyDetector(EmailAlertSender())
    assert detector_email.detectar_anomalia(lectura, 30.0) == "[email] Alerta: El valor del sensor Temp_01 excede el umbral de 30.0. Valor actual: 35.0"

"""///////////////////////////////////////// Principio 3 LISKOV SUBSTITUTION ///////////////////////////////////////////"""
def test_lsp_violation():
    temp_sensor = TemperatureSensorMal()
    assert temp_sensor.get_reading() == 25.0

    hum_sensor = HumiditySensorMal()
    with pytest.raises(ValueError):
        hum_sensor.get_reading()  # Esto debería lanzar un ValueError según la implementación de HumiditySensorMal

def test_lsp_correct():
    t_sensor = TemperatureSensor()
    h_sensor = HumiditySensor()
    assert t_sensor.get_reading() == 25.0
    assert h_sensor.get_reading() == 60.0

"""////////////////////////////////// I de SOLID/////////////////////////////////"""
def test_isp_violation():
    sensor_mal = SensorBasicoTemperaturaMal()
    assert sensor_mal.read() == 23.4
    with pytest.raises(NotImplementedError):
        sensor_mal.write(10.0)

def test_isp_correcto():
    sensor_ok = SensorBasicoTemperatura()
    assert sensor_ok.read() == 23.4

    assert not hasattr(sensor_ok, 'Write')

    smart_sensor = SensorInteligenteIndustrial()
    smart_sensor.write(45.2)
    assert smart_sensor.read() == 45.2
    assert smart_sensor.calibrate() == "Calibracion exitosa"

    """///////////////////////////////////////////////////7"""
def test_dip_violacion():
        processor_mal = DataProcessMal()
        assert hasattr(processor_mal, "_repo")
        # Corrección aquí: añade el punto antes de __name__
        assert processor_mal._repo.__class__.__name__ == "SQLServerRepository"
        
def test_dip_correcto():
        repo_falso = InMemoryRepository()
        processor = DataProcessor(repo_falso)
        lectura  = SensorReading("PRES_01",101.3,"2026-07-16 12:00")
        processor.procesar(lectura)
        ultimo = processor.obtener_ultimo("PRES_01")
        assert ultimo is not None
        assert ultimo.value == 101.3
        