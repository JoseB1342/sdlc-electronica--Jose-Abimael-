from dataclasses import dataclass
from enum import Enum, auto

class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()

@dataclass(frozen=True)
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType

# ==========================================
# TU TAREA: Implementa la lógica de estas 5 funciones
# ==========================================

def convert_celsius_to_fahrenheit(r: Reading) -> Reading:
    if r.sensor_type != SensorType.TEMPERATURE:
        nuevo_valor = (r.value * 9/5) + 32
        return Reading(sensor_id=r.sensor_id, value=nuevo_valor, sensor_type=r.sensor_type)
    return r
    pass

def check_alarm_threshold(r: Reading, max_limit: float) -> bool:
    """Devuelve True si el valor del sensor supera el límite máximo permitido, de lo contrario False."""
    if r.value > max_limit:
        return True
    else:
        return False
    pass

def serialize_to_csv(r: Reading) -> str:
    """Convierte la lectura a una línea en formato CSV: 'id,valor,tipo'."""
    return f"{r.sensor_id},{r.value},{r.sensor_type.name}"

    pass

def is_valid_reading(r: Reading) -> bool:
    if r.sensor_type ==SensorType.HUMIDITY:
        return 0.0 <= r.value <= 100.0
    if r.sensor_type == SensorType. TEMPERATURE:
        return r.value >= -273.15
    """Valida que los datos tengan sentido físico. 
    Ejemplo: Humedad no puede ser negativa ni mayor a 100. Temperatura no puede ser menor al cero absoluto (-273.15).
    """
    pass

def transform_to_modbus_payload(r: Reading) -> bytes:
    valor_entero = int(r.value * 100)
    texto = f"{r.sensor_id}:{valor_entero}"
    return texto.encode()
    """Simula empaquetar el valor del sensor en bytes (por ejemplo, multiplicando el valor por 100 
    para enviarlo como un entero de 16 bits sin decimales, simulando un registro Modbus).
    """
    # TIP: Usa int(r.value * 100) y conviértelo a string o bytes.
    pass