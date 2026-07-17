import pytest
from semana1.uart_driver.parsers import ModbusParser, NMEAParser, CanSimplificadoParser

def test_modbus_parser_valido():
    """
    Objetivo: Verificar que ModbusParser identifique y extraiga correctamente 
    los datos de una trama Modbus RTU válida (ej: bytes([0x01, 0x03, 0x00, 0x05])).
    """
    parser = ModbusParser()
    trama = bytes([0x01, 0x03, 0x00, 0x05])
    assert parser.can_parse(trama) is True
    
    resultado = parser.parse(trama)
    assert resultado["protocolo"] == "Modbus_RTU"
    assert resultado["slave_id"] == 1
    assert resultado["function_code"] == 3

def test_nmea_parser_valido():
    """
    Objetivo: Comprobar que NMEAParser procese exitosamente una cadena ASCII 
    estándar de GPS de tipo $GPGGA.
    """
    parser = NMEAParser()
    trama = b"$GPGGA,123456,1924.56,N,09654.32,W"
    assert parser.can_parse(trama) is True
    
    resultado = parser.parse(trama)
    assert resultado["protocolo"] == "NMEA_GPS"
    assert resultado["time"] == "123456"
    assert resultado["latitud"] == 1924.56

def test_can_parser_valido_y_excepcion_invalido():
    """
    Objetivo: Verificar que CanSimplificadoParser procese tramas correctas 
    y lance de forma estricta un ValueError si el DLC no coincide con los bytes reales.
    """
    parser = CanSimplificadoParser()
    # Trama CAN válida: ID=0x010A, DLC=2, Datos=[0xAA, 0xBB]
    trama_ok = bytes([0x01, 0x0A, 0x02, 0xAA, 0xBB])
    assert parser.can_parse(trama_ok) is True
    
    res = parser.parse(trama_ok)
    assert res["can_id"] == "0x10a"
    assert res["payload"] == [0xaa, 0xbb]

    # Trama corrupta: Dice que vienen 8 bytes pero la trama se corta
    trama_corrupta = bytes([0x01, 0x0A, 0x08, 0xAA])
    with pytest.raises(ValueError):
        parser.parse(trama_corrupta)