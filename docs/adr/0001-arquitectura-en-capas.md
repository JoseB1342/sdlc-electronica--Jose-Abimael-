# ADR 0001: Arquitectura en capas y Principio de Inversión de Dependencias (DIP) para SensorHub

## Estado
Aceptado

## Contexto
El proyecto SensorHub requiere procesar y almacenar datos de telemetría de manera escalable. Actualmente, existe el riesgo de acoplar fuertemente la lógica de negocio (procesamiento de datos de los sensores) con los detalles de infraestructura (base de datos SQLite, framework de red FastAPI). Necesitamos una estructura que nos permita testear la lógica del sistema de forma aislada sin levantar la infraestructura completa y que facilite futuras migraciones (por ejemplo, cambiar la base de datos a PostgreSQL cuando el volumen de lecturas aumente).

## Decisión
Se implementará una arquitectura basada en capas estrictas: `routers` -> `services` -> `repositories` -> `models`.
Para aislar la lógica de negocio, se aplicará el Principio de Inversión de Dependencias (DIP) utilizando una abstracción (`Protocol` de Python) en la capa del repositorio. El servicio dependerá de esta interfaz y no de la implementación concreta de la base de datos.

## Consecuencias

**Positivas:**
*   **Testabilidad:** Permite ejecutar pruebas unitarias de la capa de servicio utilizando dobles de prueba (*mock/fake repositories*) sin tocar la base de datos, logrando pipelines de CI/CD mucho más rápidos.
*   **Flexibilidad de Infraestructura:** Intercambiar SQLite por PostgreSQL u otra base de datos de series de tiempo no afectará ni una sola línea de código en la capa de `services`.
*   **Separación de Responsabilidades (SRP):** El router solo maneja HTTP, el servicio orquesta la lógica y el repositorio gestiona el SQL.

**Negativas:**
*   Añade complejidad inicial y mayor cantidad de archivos.
*   Implica un poco más de "ceremonia" y código repetitivo (boilerplate) para implementar operaciones CRUD simples.