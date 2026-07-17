import pytest
from dataclasses import FrozenInstanceError
from semana1.uart_driver.config import UartConfig

def test_config_construccion_valida():
    """
    Objetivo: Verificar que una configuración con parámetros válidos se instancie correctamente.
    """
    config = UartConfig(baudrate=115200, parity='N', stop_bits=1, timeout=1.0)
    assert config.baudrate == 115200
    assert config.parity == 'N'
    assert config.stop_bits == 1
    assert config.timeout == 1.0

def test_config_baudrate_invalido():
    """
    Objetivo: Comprobar que lanzar un baudrate fuera de la norma industrial levante un ValueError.
    """
    with pytest.raises(ValueError):
        # 9999 no es un baudrate UART estándar, debe tronar
        UartConfig(baudrate=9999, parity='N', stop_bits=1, timeout=1.0)

def test_config_inmutabilidad():
    """
    Objetivo: Garantizar que la configuración sea inmutable (frozen) y no pueda modificarse en caliente.
    """
    config = UartConfig(baudrate=9600, parity='E', stop_bits=2, timeout=2.0)
    
    with pytest.raises(FrozenInstanceError):
        # Intentar modificar el baudrate en caliente debe ser bloqueado por Python
        config.baudrate = 115200