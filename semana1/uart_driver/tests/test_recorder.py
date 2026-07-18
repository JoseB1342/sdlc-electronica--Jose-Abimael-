import pytest
import json
from semana1.uart_driver.recorder import DataRecorder

def test_recorder_escritura_json_lines(tmp_path):
    """
    Objetivo: Verificar que DataRecorder guarde los datos correctamente 
    en formato JSON-lines (una línea independiente por cada inserción).
    """
    # Creamos una ruta temporal para el archivo de pruebas
    archivo_prueba = tmp_path / "telemetria.jsonl"
    recorder = DataRecorder(str(archivo_prueba))
    
    dato1 = {"protocolo": "Modbus_RTU", "slave_id": 1, "value": 23.4}
    dato2 = {"protocolo": "NMEA_GPS", "latitud": 1924.56, "longitud": -9654.32}
    
    recorder.record(dato1)
    recorder.record(dato2)
    
    # Leemos el archivo físico generado para comprobar su estructura
    with open(archivo_prueba, "r", encoding="utf-8") as f:
        lineas = f.readlines()
        
    assert len(lineas) == 2
    assert json.loads(lineas[0]) == dato1
    assert json.loads(lineas[1]) == dato2

def test_recorder_error_tipo_invalido(tmp_path):
    """
    Objetivo: Comprobar que si se le pasa un dato que no sea un diccionario 
    (por ejemplo, un string o una lista), levante un TypeError de inmediato.
    """
    archivo_prueba = tmp_path / "telemetria.jsonl"
    recorder = DataRecorder(str(archivo_prueba))
    
    with pytest.raises(TypeError):
        # Pasar un string en lugar de un diccionario debe tronar
        recorder.record("Dato corrupto en texto plano")