## [27-07-2026] - Día 1: Migración a Arquitectura de Producto y FastAPI
- **Prompt/Interacción: "Ayuda para estructurar el repositorio hacia un entorno de producción (carpeta app/) y crear el primer servidor con FastAPI."
- **Resultado:** Se estableció la estructura base del sistema `SensorHub`. Se creó un `requirements.txt` curado a mano y se implementaron modelos de validación de datos (Pydantic) sin necesidad de escribir validaciones manuales.

## [27-07-2026] - Día 1: Pruebas con Swagger UI y Control de Versiones
- **Prompt/Interacción:** "Asistencia para levantar el servidor Uvicorn y probar los endpoints (GET /health y POST /readings)."
- **Resultado:** Ejecución exitosa del servidor con recarga automática (`--reload`). Se verificó la respuesta 201 y la inyección automática del ID a través de la interfaz de documentación interactiva Swagger UI, finalizando con el respaldo en GitHub.
-------------------------------------
## [28-07-2026] - Día 2: Persistencia con SQLAlchemy 2.x
- **Prompt/Interacción:** "Ayuda para conectar SQLite a la arquitectura de SensorHub e implementar modelos de persistencia."
- **Resultado:** Se configuró el motor y sesión de SQLAlchemy usando la sintaxis moderna (`Mapped`). Se logró inyectar la sesión en el endpoint POST, asegurando las transacciones ACID y guardando datos físicamente en `sensorhub.db`.
-----------------------------------------
## [29-07-2026] - Día 3: Inversión de Dependencias (DIP) y Pruebas Unitarias
- **Prompt/Interacción:** "Ayuda para implementar y probar la lógica de negocio del servicio usando un repositorio fake en memoria, aplicando el principio DIP."
- **Resultado:** Se creó la abstracción del contrato con `Protocol` y se implementó la clase `ReadingService`. Se construyó un `FakeReadingRepository` para aislar las pruebas de la base de datos y se escribieron tests exitosos en `pytest` que verifican correctamente las reglas de negocio (como el límite del cero absoluto). Las pruebas pasaron en verde priorizando la funcionalidad pura.
-------------------------------------------
## [30-07-2026] - Día 4: Inyección de Dependencias y Convenciones REST
- **Prompt/Interacción:** "Ayuda para conectar las capas del proyecto usando FastAPI, implementando los endpoints REST, paginación y manejo de errores."
- **Resultado:** Se refactorizó `main.py` eliminando rutas temporales e implementando el estándar REST (GET, POST, DELETE). Se utilizó `Depends` de FastAPI para inyectar la conexión de la base de datos hacia el repositorio, y el repositorio hacia el servicio. Se configuraron Schemas de Pydantic para proteger la API (422), manejo de errores lógicos y de búsqueda (400, 404), y se añadieron filtros de límite y fecha para optimizar las consultas GET.
-----------------------------------------------
## [31-07-2026] - Día 5: Ejercicio Integrador API SensorHub (CRUD Completo y Testing)

- **Objetivo:** Construir una API REST completa para el registro de sensores y lecturas, aplicando una arquitectura limpia de 4 capas, reglas físicas de validación y pruebas de cobertura.
- **Acciones realizadas:**
  - **Refactorización y Modelado:** Creación del modelo SQL `SensorModel` y separación estructurada de los esquemas en `schemas.py`.
  - **Validación Física (Pydantic):** Implementación de decoradores `@model_validator` para interceptar y rechazar datos físicamente imposibles (ej. temperatura < -273.15 °C o humedad > 100%) antes de tocar la base de datos (Error 422).
  - **Repositorios y Servicios:** Desarrollo de la capa de acceso a datos con soporte para *Soft Delete* (apagado lógico) y reglas de negocio para evitar colisiones de registro de sensores (Error 409).
  - **Enrutamiento (FastAPI):** Exposición de 8 endpoints REST mediante inyección de dependencias (`Depends`), disponibles y documentados en Swagger UI.
  - **Testing y Calidad (QA):** Configuración de un banco de pruebas automatizadas utilizando `pytest`, `pytest-cov` y `TestClient`. 
  - **Resolución de Bugs:** Depuración de errores de indentación (`NameError`), errores de tipeo en métodos y ajustes de aserción en las pruebas.
- **Resultado:** Sistema API backend robusto, modular y funcional. Se alcanzó exitosamente la métrica de certificación