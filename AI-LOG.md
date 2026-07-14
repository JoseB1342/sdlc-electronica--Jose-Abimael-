# Bitácora de Aprendizaje con IA - Curso Backend

## [12/07/2026] - Planificación de la Actividad 1
- **Contexto:** Configuración inicial del entorno de desarrollo y diseño de la arquitectura para mapear conceptos de hardware a software.
- **Prompt utilizado:** "¿Cómo mapear los conceptos de registros de hardware y protocolos a código idiomático en Python usando SOLID?"
- **Resultado / Aprendizaje:** Se definió una estructura basada en `Protocols` para emular los buses de comunicación (como I2C/SPI), `Dataclasses` para los paquetes de datos y `Enums` para los estados del hardware. Esto evita escribir Python como si fuera código en C estructurado.
-----------------------------------------
## [12/07/2026] Semana 1 · Entrada 1
# Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA

**Contexto:** Implementación de funciones puras sobre el dataclass inmutable `Reading` y sincronización del repositorio mediante Git.

* **Prompt enviado:**
  > "explicame como programarlos algo asi como los ejemplos que te estaba pasando anteriormente" (sobre las 5 funciones puras de conversión, umbral, CSV, validación física y empaquetado Modbus).

* **La IA propuso:**
  * Lógicas para las 5 funciones usando buenas prácticas en Python (f-strings, métodos como `.name` para enums y operaciones con floats).
  * Comandos estándar de Git para subir el código a producción (`git push origin main`).

* **Lo que acepté:**
  * La lógica de las funciones puras. En especial, el método de conversión de unidades y la simulación del empaquetado Modbus multiplicando el valor por 100 para remover decimales antes de codificarlo a bytes (`.encode()`), esto para la tranmicion de datos de forma industrial.

* **Lo que rechacé / modifiqué:**
  * **Rechazado:** El intento automático de `git push origin main`.
  * **Razón:** El servidor de GitHub rechazó el envío (`[rejected] main -> main (fetch first)`) debido a cambios concurrentes que existían en el repositorio remoto (como la creación de archivos directamente en la nube) y que no estaban sincronizados de forma local en mi computadora.
  * **Solución aplicada:** Evité usar comandos automáticos a ciegas. Corrí un `git pull origin main --allow-unrelated-histories` para fusionar de forma segura ambos historiales independientes. Resolví manualmente un conflicto menor con el nombre del archivo `AI_LOG.md`, renombrando los respaldos temporales y eliminando archivos redundantes antes de acpetar el commit de fusión final y subir mis archivos locales