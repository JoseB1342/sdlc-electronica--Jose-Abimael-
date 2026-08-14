Markdown
# AI Code Review - SensorService

**Fecha:** 12 de agosto de 2026
**Clase Auditada:** `SensorService` y `SensorRepository`

## 1. Hallazgos y Propuestas de Corrección

### Hallazgo 1: Error tipográfico (Typo) en la interfaz
* **Línea:** `def get_by_id(self, sensoir_id: str) -> SensorModel | None: ...` (En `SensorRepository`)
* **Problema:** Hay un error de tipeo en el parámetro `sensoir_id`. Esto puede causar problemas de compatibilidad o bugs silenciosos al implementar el protocolo (duck typing).
* **Corrección Propuesta:** Cambiar a `sensor_id: str`.

### Hallazgo 2: Riesgo de Rendimiento (DoS) por falta de límites
* **Línea:** `def get_all_sensors(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:`
* **Problema:** Si un usuario o API externa envía un `limit=1000000` o `limit=-1`, podría saturar la memoria del servidor o tirar la base de datos (Denegación de Servicio). No hay validación de límites numéricos.
* **Corrección Propuesta:** Limitar el tamaño máximo y validar negativos:
  ```python
  if limit <= 0 or limit > 500:
      raise ValueError("El límite debe estar entre 1 y 500")
  if offset < 0:
      raise ValueError("El offset no puede ser negativo")
  return self._repo.list_all(limit, offset)
Hallazgo 3: Casos Borde (Entradas malformadas) sin manejar
Línea: def register_sensor(self, sensor_id: str, sensor_type: str, location: str) -> SensorModel:

Problema: El tipo de dato es str, pero un string vacío "" o lleno de espacios "   " sigue siendo válido para Python. Registrar un sensor sin ID real o sin ubicación corromperá la base de datos.

Corrección Propuesta: Agregar validación rápida al inicio del método:

Python
if not sensor_id.strip() or not sensor_type.strip() or not location.strip():
    raise ValueError("Los datos del sensor no pueden estar vacíos")
Hallazgo 4: Semántica de Errores (SOLID - SRP)
Línea: raise KeyError("Sensor no encontrado en la base de datos") (En remove_sensor)

Problema: KeyError es una excepción nativa de Python pensada para diccionarios. Usarla en la capa de servicio acopla el manejo de errores a un tipo de estructura de datos subyacente.

Corrección Propuesta: Usa ValueError o, idealmente, define una excepción personalizada del dominio (ej. SensorNotFoundError(Exception)).

2. Casos de Prueba (Tests) Solicitados
Para cumplir con la métrica de cobertura y asegurar los casos borde revelados en la auditoría, se deben integrar los siguientes 5 nuevos tests al pipeline (puedes implementarlos con pytest y unittest.mock):

Test de Límite Máximo (Seguridad/Rendimiento):

Prueba: Llamar a service.get_all_sensors(limit=9999)

Expectativa: Debe lanzar ValueError evitando la consulta destructiva a la base de datos.

Test de Paginación Negativa (Caso Borde):

Prueba: Llamar a service.get_all_sensors(limit=10, offset=-5)

Expectativa: Debe lanzar ValueError por offset inválido.

Test de Registro con Strings Vacíos (Integridad de Datos):

Prueba: Llamar a service.register_sensor(sensor_id="  ", sensor_type="TMP", location="Xalapa")

Expectativa: Debe lanzar ValueError indicando que el ID no puede estar vacío.

Test de Registro de Sensor Duplicado (Lógica de Negocio):

Prueba: Configurar el mock de get_by_id para que retorne un SensorModel. Luego intentar registrar el mismo ID.

Expectativa: Debe lanzar ValueError con el mensaje de "Conflicto".

Test de Desactivación Inexistente (Manejo de Errores):

Prueba: Configurar el mock del repositorio para que deactivate() devuelva False.

Expectativa: Debe levantar la excepción correspondiente (ValueError o SensorNotFoundError) indicando que no se encontró en la DB.
