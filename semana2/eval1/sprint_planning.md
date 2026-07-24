# Sprint 1 Planning

## Sprint Goal
Construir el núcleo del sistema IoT capaz de registrar lecturas de temperatura y humedad, detectar anomalías superando umbrales estrictos y emitir alertas a través de una arquitectura escalable (Console y File).

## Historias Seleccionadas (Justificación)
Comprometido con 5 historias clave para asegurar el funcionamiento.

1. **US-01 (SensorReading):** Requisito indispensable (Must). Sin datos, no hay sistema.
2. **US-02 (AnomalyDetector):** Requisito indispensable (Must). Es la lógica de negocio central.
3. **US-03 (AlertManager):** Requisito indispensable (Must). Demuestra el uso de patrones de diseño (Strategy).
4. **US-04 (Console Alert):** Requisito indispensable (Must). Necesario para verificar que el AlertManager funciona.
5. **US-06 (SensorSimulator):** Requisito de distinción (Should). Vital para poder inyectar datos realistas y hacer pruebas de integración robustas.

## Desglose de Tareas

**US-01: SensorReading**
- Tarea 1.1: Escribir test TDD para inicialización inmutable y asignación de timestamp. (1 h)
- Tarea 1.2: Implementar clase `SensorReading` (dataclass/clase regular). (1 h)

**US-02: AnomalyDetector**
- Tarea 2.1: Escribir test TDD para inyección de umbrales en el constructor. (1 h)
- Tarea 2.2: Escribir test y lógica para detección de temperatura > 35 y humedad > 80. (2 h)

**US-03 & US-04: AlertManager y Consola**
- Tarea 3.1: Diseñar clase abstracta (Protocol o ABC) `AlertStrategy`. (1 h)
- Tarea 3.2: Implementar `ConsoleAlertStrategy` con tests TDD. (1.5 h)
- Tarea 3.3: Implementar `AlertManager` que reciba estrategias y despache eventos. (1.5 h)

**US-06: SensorSimulator (Extensión)**
- Tarea 6.1: Crear clase generadora usando `random.gauss` para temperatura y humedad. (2 h)
- Tarea 6.2: Construir el Test de Integración (10 sensores x 60 ciclos). (3 h)

## Definition of Done (DoD)
- Los criterios de aceptación están implementados como pruebas en `pytest`.
- La cobertura de código es mayor o igual al 80%.
- El linter (`ruff`) y análisis de tipado (`mypy`) no reportan errores.
- Todas las historias completadas están integradas en la rama principal.