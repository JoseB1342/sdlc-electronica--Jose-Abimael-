# Curso Backend - Especialización en Sistemas de Información (EDSIA)

---------------------------

##  Stack Tecnológico
Este proyecto está construido utilizando las siguientes herramientas profesionales:

* **Lenguaje:** Python 3.12+ (con Type Hints avanzados, Dataclasses y Enums)
* **Framework API:** FastAPI
* **ORM & Migraciones:** SQLAlchemy 2.x + Alembic
* **Base de Datos:** SQLite / PostgreSQL (vía Docker)
* **Calidad de Código & Linters:** Ruff + mypy
* **Pruebas Automatizadas:** pytest + pytest-cov + httpx
* **Contenedores:** Docker + Docker Compose
* **Asistentes de IA:** GitHub Copilot / Aider (Bitácora en `AI_LOG.md`)
* -------------------------
## Introduccion a SCRUM
**¿Qué es?**
    * SCRUM es un lugar de trabajo en donde se ayuda a equipos a desarrollar y mejorar productos de una manera interativa e incremental. Principlamente se basa en el cambio adaptativo y la entrga. 

**Los 3 pilares de SCRUM**
    * Transparencia: Toda la información importante debe ser visible para el equipo.
    * Inspección: El trabajo y los resultados se revisan constantemente para detectar problemas.
    * Adaptación: Cuando se identifican cambios o problemas, el equipo ajusta su forma de trabajar.

**Los 5 valores de SCRUM**
    * Compromiso: El equipo se compromete con los objetivos.
    * Enfoque: Se trabaja en las tareas más importantes del Sprint.
    * Apertura: Se comparte información y se aceptan nuevas ideas.
    * Respeto: Todos los integrantes valoran el trabajo de los demás.
    * Valentía: Se enfrentan retos y se toman decisiones difíciles cuando es necesario.

**Roles de SCRUM**
* Product Owner
    Define qué necesita el producto.
    Prioriza las tareas mediante el Product Backlog.
    Busca maximizar el valor del producto.
* Scrum Master
    Ayuda al equipo a seguir Scrum correctamente.
    Elimina obstáculos que afectan el trabajo.
    Facilita reuniones y promueve la mejora continua.
* Developers (Desarrolladores)
    Construyen el producto.
    Planifican el trabajo del Sprint.
    Se organizan de forma autónoma.

**Eventos de SRUM**
- **Sprint:** Hasta 1 mes.
- **Sprint Planning:** Máximo 8 horas para un Sprint de 1 mes.
- **Daily Scrum:** 15 minutos.
- **Sprint Review:** Máximo 4 horas para un Sprint de 1 mes.
- **Sprint Retrospective:** Máximo 3 horas para un Sprint de 1 mes.

**Artefactos y sus compromisos**
- **Product Backlog** Objtivo del producto
- **Srpint Backlog** Objetivo del sprint
- **Increment** Definicion del echo (Definition fo Done)

**Deferencia entre Definition of Done y criterio de acpetacion**
* Definition of Done                         Citerios e acpetacion
- Aplica a todo el incremento.               - Aplica una historia de usuario especifica.
- Define la calidad general del trabajo.     - Define la funcionalidad esperada de un requisito.
- Es estable y compartida de todo el grupo.  - Cambia segun cada historia del usuario.