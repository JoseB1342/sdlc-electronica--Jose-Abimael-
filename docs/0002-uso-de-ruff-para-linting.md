# ADR 0002: Uso de Ruff para análisis estático y formateo

## Estado
Aceptado

## Contexto
Para mantener el código limpio, estandarizado y que el CI/CD en GitHub Actions no permitiera subir "código sucio", necesitábamos herramientas de formateo y análisis estático (linting). Tradicionalmente se usarían múltiples herramientas (Flake8, Black, isort).

## Decisión
Decidimos adoptar **Ruff** como nuestra única herramienta centralizada para el formateo de código, orden de imports y linting en el pipeline de GitHub Actions.

## Consecuencias
* **Positivas:** La ejecución en el pipeline de CI/CD es casi instantánea por estar escrito en Rust. Reemplazó a 3 herramientas distintas, simplificando la configuración (`pyproject.toml`).
* **Negativas:** Es extremadamente estricto por defecto, requiriendo silenciar errores específicos en archivos auto-generados por herramientas como Alembic (`# ruff: noqa`).