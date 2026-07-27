## [27-07-2026] - Día 1: Migración a Arquitectura de Producto y FastAPI
- **Prompt/Interacción: "Ayuda para estructurar el repositorio hacia un entorno de producción (carpeta app/) y crear el primer servidor con FastAPI."
- **Resultado:** Se estableció la estructura base del sistema `SensorHub`. Se creó un `requirements.txt` curado a mano y se implementaron modelos de validación de datos (Pydantic) sin necesidad de escribir validaciones manuales.

## [27-07-2026] - Día 1: Pruebas con Swagger UI y Control de Versiones
- **Prompt/Interacción:** "Asistencia para levantar el servidor Uvicorn y probar los endpoints (GET /health y POST /readings)."
- **Resultado:** Ejecución exitosa del servidor con recarga automática (`--reload`). Se verificó la respuesta 201 y la inyección automática del ID a través de la interfaz de documentación interactiva Swagger UI, finalizando con el respaldo en GitHub.