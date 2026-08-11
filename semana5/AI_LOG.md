## Actividad Semana 5: Implementación con IA y Trazabilidad

**Herramienta designada:** Aider CLI (Ejecución fallida por bloqueos de entorno)
**Herramienta de contingencia utilizada:** Copilot Chat / LLM Asistente

**Reporte Técnico de Incidencias (Troubleshooting):**
Durante la configuración de Aider en el entorno local (Windows, Python 3.12), se presentaron bloqueos sistémicos en cadena que impidieron su uso operativo:
1. **Fallo de Enrutamiento API (Bug Upstream):** La versión actual de Aider (v0.86.2) presenta un bug interno en su librería `litellm`. Forzó el enrutamiento del modelo `gemini-1.5-pro` hacia servidores de Vertex AI, arrojando un error constante `404 NOT_FOUND (Vertex_ai_betaException)` e invalidando la API Key legítima de AI Studio.
2. **Dependencias Retiradas (Yanked):** Al intentar un *downgrade* a versiones más estables (0.72.0 y 0.80.0) utilizando el gestor `uv`, la instalación falló porque paquetes críticos (`configargparse==1.7` y `aiohttp==3.11.14`) fueron retirados de los repositorios oficiales por sus desarrolladores debido a regresiones.
3. **Bloqueo por Compilación C++:** Al utilizar una resolución dinámica de dependencias (`aider-chat<0.86.0`), el sistema intentó compilar el paquete `cffi` desde el código fuente, exigiendo la instalación de *Microsoft Visual C++ 14.0 Build Tools*.

**Decisión Técnica:** Aplicando el principio de *Timeboxing*, se abortó la instalación de Aider para evitar instalar dependencias y compiladores C++ innecesarios en el entorno. Se procedió a utilizar el plan de contingencia, generando el código de manera externa y registrando la trazabilidad de la IA mediante commits manuales en Git.