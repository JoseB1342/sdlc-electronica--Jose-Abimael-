# Laboratorio de Prompting - Semana 5

## Tarea 1: Calcular promedio de lecturas de sensores

### Prompt Pobre
"Crea una función para sacar el promedio de los sensores."

**Resultado del Prompt Pobre:**
def promedio_sensores(sensores):
    total = 0
    for sensor in sensores:
        total += sensor.valor
    return total / len(sensores)

---

### Prompt Bueno
CONTEXTO: API FastAPI (Python 3.12) para gestion de sensores.
          SQLAlchemy 2.x tipado, arquitectura en capas.
TAREA: Escribe una funcion pura calculate_reading_average(readings: list[ReadingModel]) -> float
       en app/utils/math_utils.py.
RESTRICCIONES: type hints completos, docstring, manejar el caso de lista vacia 
               levantando un ValueError, ignorar lecturas nulas, redondeo a 2 decimales.
               No usar dependencias externas.
ENTREGA: solo la funcion, sin explicacion.

**Resultado del Prompt Bueno:**
def calculate_reading_average(readings: list['ReadingModel']) -> float:
    """
    Calcula el promedio de los valores numéricos de una lista de lecturas.
    
    Ignora aquellas lecturas cuyo valor sea None.
    
    Args:
        readings (list[ReadingModel]): Lista de objetos de lectura del sensor.
        
    Returns:
        float: Promedio de los valores redondeado a 2 decimales.
        
    Raises:
        ValueError: Si la lista original está vacía o si no contiene valores válidos.
    """
    if not readings:
        raise ValueError("No se puede calcular el promedio: la lista de lecturas está vacía.")
        
    valid_values = [reading.value for reading in readings if reading.value is not None]
    
    if not valid_values:
        raise ValueError("No se puede calcular el promedio: no hay valores válidos en la lista.")
        
    average = sum(valid_values) / len(valid_values)
    return round(average, 2)

## Tarea 2: Refactorizar validación de unidades físicas

### Prompt Pobre
"Saca la validación de las unidades a otra función."

**Resultado del Prompt Pobre:**
```python
def validar_unidades(unidad):
    if unidad == "CELSIUS" or unidad == "HUMEDAD" or unidad == "HPA":
        return True
    else:
        return False

CONTEXTO: API FastAPI (Python 3.12) para gestion de sensores. SQLAlchemy 2.x tipado, Pydantic para esquemas.
TAREA: Extrae la validacion de unidades fisicas (CELSIUS, HUMEDAD, HPA) a una funcion pura independiente validate_physical_unit(unit: str) -> bool en app/utils/validators.py.
RESTRICCIONES: type hints completos, docstring. Si la unidad no es valida, debe levantar un ValueError con un mensaje descriptivo que incluya la unidad rechazada. No usar librerias externas.
ENTREGA: solo la funcion, sin explicacion.

**Resultado promt bueno:**
def validate_physical_unit(unit: str) -> bool:
    """
    Valida que la unidad física de la lectura sea una de las permitidas por el sistema.
    
    Args:
        unit (str): La unidad física a validar (ej. CELSIUS, HUMEDAD, HPA).
        
    Returns:
        bool: True si la unidad es válida.
        
    Raises:
        ValueError: Si la unidad recibida no pertenece a las métricas autorizadas.
    """
    valid_units = {"CELSIUS", "HUMEDAD", "HPA"}
    
    if not isinstance(unit, str):
        raise ValueError(f"La unidad debe ser una cadena de texto, se recibió: {type(unit).__name__}")
        
    unit_upper = unit.upper().strip()
    
    if unit_upper not in valid_units:
        raise ValueError(f"Unidad no permitida: '{unit}'. Valores aceptados: {', '.join(valid_units)}")
        
    return True

## Tarea 3: Generar prueba unitaria con Pytest

### Prompt Pobre
"Haz un test para la funcion de promedios si le paso una lista vacia."

**Resultado del Prompt Pobre:**
```python
def test_promedio():
    lista = []
    resultado = calculate_reading_average(lista)
    if resultado == 0:
        print("Test pasó")

Prompt Bueno
CONTEXTO: Proyecto con FastAPI y Pytest. Se tiene la función calculate_reading_average(readings: list['ReadingModel']) en app/utils/math_utils.py que debe levantar un ValueError si la lista está vacía.
TAREA: Escribe una prueba unitaria usando Pytest para validar el escenario de la lista vacía.
RESTRICCIONES: Usar el manejador de contexto pytest.raises para atrapar la excepción. Incluir un docstring claro y type hints (-> None). Nombra la función de prueba siguiendo las mejores prácticas (descriptiva).
ENTREGA: solo el código de la prueba, sin explicación.

Resultado del Prompt Bueno:
import pytest
from app.utils.math_utils import calculate_reading_average

def test_calculate_reading_average_raises_value_error_on_empty_list() -> None:
    """
    Verifica que la función levante adecuadamente un ValueError 
    cuando se le pasa una lista de lecturas vacía.
    """
    with pytest.raises(ValueError, match="la lista de lecturas está vacía"):
        empty_readings: list = []
        calculate_reading_average(empty_readings)