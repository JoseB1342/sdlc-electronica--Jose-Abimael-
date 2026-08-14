## Actividad Semana 5: Implementación con IA y Trazabilidad

**Herramienta designada:** Aider CLI (Ejecución fallida por bloqueos de entorno)
**Herramienta de contingencia utilizada:** Copilot Chat / LLM Asistente

**Reporte Técnico de Incidencias (Troubleshooting):**
Durante la configuración de Aider en el entorno local (Windows, Python 3.12), se presentaron bloqueos sistémicos en cadena que impidieron su uso operativo:
1. **Fallo de Enrutamiento API (Bug Upstream):** La versión actual de Aider (v0.86.2) presenta un bug interno en su librería `litellm`. Forzó el enrutamiento del modelo `gemini-1.5-pro` hacia servidores de Vertex AI, arrojando un error constante `404 NOT_FOUND (Vertex_ai_betaException)` e invalidando la API Key legítima de AI Studio.
2. **Dependencias Retiradas (Yanked):** Al intentar un *downgrade* a versiones más estables (0.72.0 y 0.80.0) utilizando el gestor `uv`, la instalación falló porque paquetes críticos (`configargparse==1.7` y `aiohttp==3.11.14`) fueron retirados de los repositorios oficiales por sus desarrolladores debido a regresiones.
3. **Bloqueo por Compilación C++:** Al utilizar una resolución dinámica de dependencias (`aider-chat<0.86.0`), el sistema intentó compilar el paquete `cffi` desde el código fuente, exigiendo la instalación de *Microsoft Visual C++ 14.0 Build Tools*.

**Decisión Técnica:** Aplicando el principio de *Timeboxing*, se abortó la instalación de Aider para evitar instalar dependencias y compiladores C++ innecesarios en el entorno. Se procedió a utilizar el plan de contingencia, generando el código de manera externa y registrando la trazabilidad de la IA mediante commits manuales en Git.
------------------------------------------------
# AI Code Review - SensorService

**Fecha:** 12 de agosto de 2026
**Archivo Auditado:** `app/services/sensor_service.py`
**Herramienta IA:** Copilot Chat / LLM (Asistente)

## 1. Hallazgos y Correcciones Implementadas

Durante la revisión de código como ingeniero senior apoyada por IA, se detectaron y corrigieron los siguientes problemas de robustez, principios SOLID y casos borde:

*   **Hallazgo 1: Error tipográfico (Typo) en la interfaz `SensorRepository`**
    *   **Problema:** El parámetro en el método `get_by_id` estaba escrito como `sensoir_id`, lo cual puede generar bugs silenciosos al implementar el protocolo (duck typing).
    *   **Estado:** Aceptado e implementado. Se corrigió la firma del método a `sensor_id: str`.

*   **Hallazgo 2: Casos Borde (Entradas malformadas) sin manejar**
    *   **Problema:** El método `register_sensor` declaraba tipos `str`, pero permitía registrar sensores con strings vacíos o con puros espacios (ej. `"   "`), lo que corrompería la base de datos.
    *   **Estado:** Aceptado e implementado. Se agregó validación con `.strip()` al inicio del método; si los datos están vacíos, arroja un `ValueError`.

*   **Hallazgo 3: Riesgo de Rendimiento (DoS) por falta de límites**
    *   **Problema:** El método `get_all_sensors` no validaba el tamaño de `limit` ni `offset`. Un actor malicioso podría solicitar millones de registros (`limit=1000000`) o usar números negativos, saturando la memoria o la base de datos.
    *   **Estado:** Aceptado e implementado. Se limitó el rango de consulta (1 a 500) y se prohibieron offsets negativos.

*   **Hallazgo 4: Semántica de Errores Inadecuada (Violación de SRP)**
    *   **Problema:** `remove_sensor` utilizaba `KeyError` (excepción nativa de diccionarios en Python) al no encontrar un sensor, acoplando la lógica de la capa de servicio a una estructura de datos específica.
    *   **Estado:** Aceptado e implementado. Se reemplazó por un `ValueError` estándar que se adapta mejor a la capa de dominio.

## 2. Cobertura de Pruebas Integradas

Para garantizar la fiabilidad del código y probar los casos borde descubiertos durante la auditoría, se integraron **5 nuevas pruebas unitarias** en el pipeline (`tests/test_sensor_service.py`) utilizando `pytest` y `unittest.mock`:

1.  `test_get_all_sensors_limite_excedido`: Verifica la protección del sistema al exceder el límite de 500 registros.
2.  `test_get_all_sensors_offset_negativo`: Verifica que el sistema bloquee intentos de paginación negativa.
3.  `test_register_sensor_datos_vacios`: Asegura el rechazo de inserciones con strings vacíos.
4.  `test_register_sensor_duplicado`: Valida la lógica de negocio al intentar registrar un ID de sensor previamente existente (usando mocks).
5.  `test_remove_sensor_inexistente`: Valida que la capa de servicio arroje la excepción correcta cuando el repositorio no logra desactivar un sensor.
-------------------------------------
## [14-08-2026] - Actividad del dia viernes
1° Prompt: "Modifica ReadingService para inyectar alert_strategy y evaluar si la lectura supera el max_threshold. Si lo supera, genera una alerta y llama a send_alert."

Qué generó: El código actualizado de ReadingService con la inyección de dependencias y la validación del umbral.

Qué cambiaste y por qué: "Tuve que corregir el FakeReadingRepository agregando self._storage.append(reading) para que las pruebas anteriores no fallaran debido al estado del mock."

2° Prompt: Solicité una prueba para el endpoint GET /sensors/{sensor_id}/alerts esperando un 200 OK y una lista.

Qué generó: Una prueba usando el TestClient de FastAPI.

Qué cambiaste y por qué: Tuve que mover la prueba de test_services.py a test_main.py para tener acceso al client configurado, y comprobé que falla con un 404 (Fase Roja).

3° Prompt: "Crear AlertModel en SQLAlchemy, implementar DBAlertStrategy que guarde en base de datos, y crear el endpoint GET /sensors/{sensor_id}/alerts."

Qué generó: El modelo de base de datos, la nueva estrategia concreta y el router de FastAPI.

Qué cambiaste y por qué: "Tuve que borrar el archivo .db local para que SQLAlchemy aplicara la nueva tabla de alertas. Al ejecutar las pruebas, todo pasó a verde."