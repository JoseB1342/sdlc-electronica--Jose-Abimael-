# Registro de Uso de Inteligencia Artificial (AI Log)

Durante el desarrollo y despliegue de SensorHub, utilicé Inteligencia Artificial (LLMs) como asistente de depuración (debugging) y configuración de infraestructura. A continuación, se documentan dos instancias clave:

## 1. Resolución de conflictos entre Alembic y Ruff (Linter)
* **El Problema:** El pipeline de CI/CD en GitHub Actions fallaba porque Ruff detectaba errores de formato (I001, E402) en los archivos auto-generados por Alembic en la carpeta `migrations/`.
* **Uso de la IA:** Le pasé los logs de error de la terminal a la IA para entender por qué Git no detectaba mis cambios locales.
* **Sugerencia Aplicada:** Utilizar el comentario `# ruff: noqa` en la cabecera de los archivos auto-generados para ignorar las reglas de linting, ya que Alembic los formatea con sus propios estándares.
* **Sugerencia Descartada:** Descarté la opción inicial de arreglar los imports manualmente línea por línea, ya que cada vez que Alembic generara una nueva migración, el problema volvería a aparecer.

## 2. Depuración de conexión a PostgreSQL en Render
* **El Problema:** El despliegue fallaba en la nube de Render arrojando un error de SQLAlchemy: `Connection refused a 127.0.0.1 (localhost)`.
* **Uso de la IA:** Proporcioné los logs de despliegue de Render para analizar la caída del servicio. La IA identificó que Alembic estaba usando la configuración quemada de `alembic.ini` en lugar de la variable de entorno de la nube.
* **Sugerencia Aplicada:** Modificar `migrations/env.py` para inyectar dinámicamente `os.getenv("DATABASE_URL")` y reemplazar el prefijo `postgres://` por `postgresql+psycopg://` requerido por SQLAlchemy 2.0.