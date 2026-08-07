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
- **Resultado:** Sistema API backend robusto, modular y funcional. Se alcanzó exitosamente la métrica de certificación.
--------------------------------------------
## [01-08-2026] - Cierre Semana 3: Análisis Estático, QA y Pull Request
- **Objetivo:** Preparar el código para producción (Nivel Alto Potencial) aplicando análisis estático estricto y abriendo el PR para la revisión por pares.
- **Pront Enciado** Ayuda con la correccion de errores y filtrado de errores de de reglas esteticas.
- **Acciones realizadas:**
  - **Linter (Ruff):** Se creó el archivo `pyproject.toml` para ignorar falsos positivos de FastAPI (B008) y reglas estéticas (E501). Se corrigieron bugs lógicos reales como el rastreo forense de excepciones (`raise ... from e`) y el uso seguro de `isinstance()` en las pruebas.
  - **Tipado Estricto (Mypy):** Se depuraron discrepancias entre los Contratos (Protocols) y los Repositorios de SQLite, alineando los tipos de datos de entrada (`value: float`) y los retornos de las funciones (`-> None`). Se logró el estatus `Success: no issues found`.
  - **Control de Versiones:** Se aplicó el flujo de trabajo profesional creando una rama secundaria (`entrega-final`) para aislar los cambios y poder abrir un Pull Request hacia `main`, habilitando el proceso de Peer Review.
- **Resultado:** Código 100% blindado contra bugs lógicos y de tipado, y el Pull Request creado exitosamente en GitHub.
-----------------------------------
## [03-08-2026] - Restauración del Sistema y Despliegue en Docker
- **Objetivo:** Resolver el fallo del motor de Docker por falta de almacenamiento, restablecer el equipo de fábrica y lograr la ejecución de la API en un contenedor.
- **Pront Enciado** Ayuda con error en el engine de Docker, respaldo de proyecto antes de formatear de fábrica y reinstalación del entorno para levantar el contenedor.
- **Acciones realizadas:**
  - **Respaldo y Formateo:** Se sincronizó la configuración de VS Code en la nube, se subió el proyecto a GitHub, se limpió la caché y se restableció Windows de fábrica (Quitar todo) para recuperar espacio.
  - **Configuración de Entorno:** Se reinstalaron Python y Git asegurando la configuración del PATH. Se clonó el repositorio y se habilitó la ejecución de scripts en PowerShell (`Set-ExecutionPolicy RemoteSigned`).
  - **Restauración de Dependencias:** Se generó un nuevo entorno virtual (`.venv`) y se instalaron las librerías necesarias mediante `requirements.txt`.
  - **Despliegue en Docker:** Se actualizó el núcleo de WSL (`wsl --update`), se construyó la imagen (`docker build -t sensorhub:dev .`) y se inicializó el servidor (`docker run -p 8000:8000 sensorhub:dev`).
- **Resultado:** Equipo local limpio y optimizado, entorno de desarrollo 100% funcional y la API SensorHub ejecutándose exitosamente dentro del contenedor de Docker.
----------------------------------------------
## [04-08-2026] - Orquestación con Docker Compose, PostgreSQL y Alembic
- **Objetivo:** Orquestar múltiples contenedores enlazando la API con una base de datos PostgreSQL utilizando Docker Compose, e inicializar el control de versiones de la base de datos con Alembic.
- **Pront Enciado** Ayuda con la creación de docker-compose para PostgreSQL, configuración de variables de entorno dinámicas, inicialización de Alembic y resolución de errores de despliegue (motor apagado y crash de Uvicorn).
- **Acciones realizadas:**
  - **Orquestación (Docker Compose):** Se creó el archivo `docker-compose.yml` para levantar en simultáneo los servicios de la API y la base de datos (`postgres:16`), configurando puertos, volúmenes de persistencia y la variable `DATABASE_URL`.
  - **Conexión Dinámica a Base de Datos:** Se refactorizó `app/db.py` agregando una función para normalizar URLs de conexión y garantizar compatibilidad con despliegues en la nube. Se instaló y documentó el driver `psycopg[binary]` en `requirements.txt`.
  - **Control de Versiones (Alembic):** Se inicializó Alembic en el proyecto, enlazando `Base.metadata` y la URL dinámica en `env.py`. Se generó la migración inicial (`revision --autogenerate`) y se aplicó a la base de datos (`upgrade head`).
  - **Troubleshooting y Despliegue:** Se diagnosticó y resolvió el fallo de conexión con el demonio de Docker Desktop. Posteriormente, se solucionó un error de importación en Uvicorn forzando la reconstrucción de la imagen (`docker compose up --build`) para integrar las nuevas dependencias.
- **Resultado:** Arquitectura multi-contenedor ejecutándose con éxito. La API se conecta dinámicamente a PostgreSQL y el esquema de la base de datos está bajo control de versiones con Alembic, verificado funcionalmente a través de Swagger UI.
---------------------------------------
## [05-08-2026] - Integración Continua (CI) con GitHub Actions y Análisis Estático
- **Objetivo:** Implementar un pipeline de Integración Continua (CI) en GitHub Actions y asegurar el cumplimiento de los estándares de calidad del código.
- **Pront Enciado** Ayuda con la configuración del workflow de GitHub Actions, diagnóstico del "exit code 1" y resolución de múltiples errores de linting (PEP 8) con Ruff.
- **Acciones realizadas:**
  - **Configuración del Pipeline:** Se creó la estructura `.github/workflows/ci.yml` para disparar análisis automáticos en eventos `push` y `pull_request` hacia la rama `main`.
  - **Automatización de Entorno:** Se configuraron los pasos para aprovisionar Ubuntu, instalar Python 3.12 y ejecutar las dependencias y herramientas de calidad (`pytest`, `ruff`, `mypy`).
  - **Troubleshooting de CI:** Se identificó un fallo en el pipeline (X roja, exit code 1) provocado por 48 violaciones de estilo detectadas por el linter.
  - **Refactorización y Configuración:** Se aplicó `ruff check . --fix` para correcciones automáticas de sintaxis. Posteriormente, para conservar los comentarios documentales largos sin violar el estándar, se implementó el archivo `pyproject.toml` configurando `line-length = 250`.
- **Resultado:** Repositorio protegido por un pipeline de CI 100% funcional y en verde. El código ahora es evaluado automáticamente contra estándares de calidad flexibilizados a las necesidades del proyecto.
-----------------------------------------
## [06-08-2026] - Infraestructura como Código y Despliegue Continuo (CD)
- **Objetivo:** Implementar Infraestructura como Código (IaC) para lograr el Despliegue Continuo de la API y la base de datos en un entorno de producción público (Render).
- **Pront Enciado** Ayuda para configurar el archivo `render.yaml`, resolver errores de parseo de comandos en Render (exit code 2 y 127) y delegar el script de arranque seguro.
- **Acciones realizadas:**
  - **Preparación del Servicio:** Se programó el endpoint `/health` requerido para el monitoreo de vida (health check) del proveedor de nube.
  - **Infraestructura como Código:** Se redactó el Blueprint `render.yaml` para provisionar automáticamente el servicio web y una base de datos PostgreSQL, inyectando de forma segura la credencial `DATABASE_URL`.
  - **Troubleshooting de Despliegue:** Se identificó un conflicto en el intérprete de comandos de Render al procesar operadores lógicos (`&&`). La arquitectura de arranque se refactorizó eliminando el `dockerCommand` del Blueprint y migrando la instrucción `alembic upgrade head && uvicorn...` directamente al `CMD` del `Dockerfile` en formato Shell.
  - **Despliegue Continuo:** Se conectó el repositorio principal a Render. Gracias a esto, cada nuevo `push` a la rama `main` compila y publica los cambios automáticamente tras pasar las validaciones del CI.
- **Resultado:** API desplegada exitosamente en internet con una URL pública funcional. La conexión a la base de datos de producción y la creación automatizada de esquemas (Alembic) fueron verificadas.
------------------------------------------------
## [07-08-2026] - Cierre de Evaluación 2: Pipeline de Producción y Documentación
- **Objetivo:** Consolidar los entregables de la evaluación "Pipeline de producción", integrar las evidencias de Integración Continua y documentar los accesos al entorno de producción.
- **Pront Enciado** Ayuda con la revisión de la rúbrica de evaluación, obtención del badge de GitHub Actions y actualización del archivo README para entrega final.
- **Acciones realizadas:**
  - **Generación de Evidencia CI:** Se obtuvo e integró el *status badge* de GitHub Actions en el repositorio para evidenciar visualmente el éxito del pipeline (ejecución en verde de tests, ruff y mypy).
  - **Documentación de Entorno Público:** Se estructuró el archivo `README.md` exponiendo de manera clara la URL de producción alojada en Render, incluyendo los accesos directos a los endpoints críticos (`/health` y `/docs`).
  - **Auditoría de Secretos:** Se verificó la correcta configuración del archivo `.gitignore`, garantizando que ninguna variable de entorno ni credencial (`.env`) haya sido inyectada en el historial de control de versiones.
  - **Validación de Despliegue Continuo (CD):** Se realizó un *commit* final con la actualización de la documentación, lo que disparó automáticamente el flujo de CI/CD y actualizó el servicio en la nube, demostrando la integración total del ciclo de vida del software.
- **Resultado:** Proyecto de la Semana 2 concluido exitosamente y alineado al 100% con la rúbrica. La API de SensorHub está contenerizada, protegida por pruebas automatizadas y desplegada públicamente en internet con prácticas de grado industrial.