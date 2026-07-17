import pytest
from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import ModbusParser, NMEAParser
from semana1.uart_driver.device import UartDevice

def test_device_error_no_conectado():
    """
    Objetivo: Garantizar que si se intenta leer datos sin conectar el dispositivo,
    se levante un RuntimeError de forma estricta.
    """
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    device = UartDevice(config=config, parsers=[ModbusParser()])
    
    with pytest.raises(RuntimeError):
        device.read_and_parse()

def test_device_parsing_exitoso_inyectado():
    """
    Objetivo: Validar el flujo DIP completo. Conectar dispositivo, inyectar datos en 
    el buffer circular mediante hilos/simulación y parsear exitosamente usando Modbus.
    """
    config = UartConfig(baudrate=115200, parity='N', stop_bits=1, timeout=1.0)
    parsers = [ModbusParser(), NMEAParser()]
    device = UartDevice(config=config, parsers=parsers)
    
    device.connect()
    
    # Simulamos la llegada de una trama Modbus válida al buffer
    trama_modbus = bytes([0x01, 0x03, 0x10, 0x20])
    device.simulate_hardware_interrupt(trama_modbus)
    
    resultado = device.read_and_parse()
    assert resultado is not None
    assert resultado["protocolo"] == "Modbus_RTU"
    assert resultado["slave_id"] == 1

def test_device_protocolo_desconocido():
    """
    Objetivo: Verificar que si el buffer circular recibe bytes de basura 
    o un protocolo no registrado en la inyección de dependencias, levante un ValueError.
    """
    config = UartConfig(baudrate=9600, parity='N', stop_bits=1, timeout=1.0)
    device = UartDevice(config=config, parsers=[ModbusParser()])
    
    device.connect()
    
    # Una trama que inicia con 0xFF no es válida para ModbusParser
    trama_invalida = bytes([0xFF, 0xAA, 0xBB])
    device.simulate_hardware_interrupt(trama_invalida)
    
    with pytest.raises(ValueError):
        device.read_and_parse()