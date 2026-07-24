# Sprint 1 Retrospective - IoT Sistema de monitoreo

## ¿Qué salió bien?
- La implementación de TDD (Rojo-Verde-Refactor) aseguró que el código del núcleo funcionara correctamente desde el primer intento.
- El uso del Patrón Strategy para el `AlertManager` dejó una arquitectura muy limpia y fácil de expandir sin tocar el código existente.
- Se superó el 80% de cobertura y se cumplió con las reglas estrictas de tipado de `mypy`.

## ¿Qué se puede mejorar?
- Hubo fricción al final del sprint con las herramientas de calidad (Ruff y Mypy). Los errores de estilo (como líneas largas o importaciones duplicadas/desordenadas) se acumularon y causaron fallos en la canalización (pipeline) local.
- **Validación de Hardware:** El `SensorReading` confía ciegamente en los datos. Un sensor dañado podría enviar valores físicamente imposibles y el sistema los procesaría sin problemas.

## Acción concreta para el próximo Sprint
- **Ejecutar linters tempranamente:** Ejecutar `ruff check --fix` después de cada ciclo "Refactor" de TDD en lugar de esperar hasta el final de la historia de usuario. Esto evitará la acumulación de advertencias (warnings) de estilo.
- **Defensa contra Hardware:** Agregar validación de límites físicos en el inicializador del dataclass `SensorReading`.