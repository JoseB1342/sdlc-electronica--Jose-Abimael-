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

* **Lo que rechace / modifiqué:**
  * **Rechazado:** El intento automático de `git push origin main`.
  * **Razón:** El servidor de GitHub rechazó el envío (`[rejected] main -> main (fetch first)`) debido a cambios concurrentes que existían en el repositorio remoto (como la creación de archivos directamente en la nube) y que no estaban sincronizados de forma local en mi computadora.
  * **Solución aplicada:** Evité usar comandos automáticos a ciegas. Corrí un `git pull origin main --allow-unrelated-histories` para fusionar de forma segura ambos historiales independientes. Resolví manualmente un conflicto menor con el nombre del archivo `AI_LOG.md`, renombrando los respaldos temporales y eliminando archivos redundantes antes de acpetar el commit de fusión final y subir mis archivos locales
  --------------------------------
  ## [14/07/2026] Semana 1 · Entrada 2
  # Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA

  **Contexto** Diseño de una Máquina de Estados Finitos (FSM) secuencial para la simulación de un semáforo de tráfico y verificación mediante pytest.
  >Solicitudes de guía para estructurar una clase en Python que controle transiciones de estado deterministas y acumule métricas de ciclos, junto con la configuración de sus pruebas unitarias.

  * **La IA propuso**
   * Una estructura de clase básica con métodos de actualización de estado y variables de instancia para almacenar el estado actual como un string.
   * Cuatro pruebas unitarias para validar el estado inicial, la transición simple, el ciclo completo y el incremento del contador.

  * **Lo que acepté**
    * La lógica de transición secuencial encapsulada en un método estructurado, lo cual simula perfectamente el comportamiento de un lazo de control en un sistema embebido.
    * La arquitectura de las pruebas con pytest para aislar fallos de lógica antes de llevar el diseño a simulación física

  * **Lo que rechace**
    * La propuesta inicial de usar strings libres para los estados sin validación rigurosa, lo cual permitía estados inválidos por errores de tipeo.

  * **Lo que modifique**
    * Modifiqué la estructura implementando propiedades de lectura o validaciones explícitas para asegurar que la máquina solo acepte los estados predefinidos.
    * Ajusté los nombres de las funciones en el archivo semana1/test_fsm.py para asegurar condiciones de frontera estrictas (como validar que el contador inicie exactamente en 0 y se incremente solo al cerrar el ciclo en RED).

  * **Resultado**
    * La FSM fue verificada exitosamente en la terminal logrando los primeros 4 PASSED de la suite de pruebas.
  --------------------------------
  ## [16/07/2026] Semana 1 · Entrada 3
  # Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA

  **Contexto** Implementacion y verificacion de pruebas automatizadas con (pytest) de los principios SPR, OCP, LSP aplicados en sensores.
* **Pront enviado:** 
>"Solicitudes consecutivas para corregir la sintaxis de Python en el diseño de las clases y     estructurar la suite de pruebas unitarias exactas (==) basadas en strings de telemetría industrial."

  * **La IA propuso**
    * Estructuras de código para los ejemplos "mal" y "bien" de los principios de Responsabilidad Única, Abierto/Cerrado y Sustitución de Liskov.
    * Diseños iniciales de pruebas que utilizaban instrucciones print() dentro de las alertas y comparaciones parciales basadas en el operador in.

  * **Lo que acepte**
    * El diseño de la arquitectura modular. Separar la adquisición de hardware (SensorReader) del almacenamiento (DataLogger) para SRP, y el uso de interfaces abstractas (ABC) con polimorfismo en AlertSender para desacoplar el detector de anomalías de los canales de salida para OCP.
    * El principio de sustitución de Liskov (LSP) garantizando que las subclases de sensores mantengan el contrato de tipos de datos (float) de forma intercambiable.

  * **Lo que rechace**
    * La implementación de efectos secundarios como print() o la apertura de archivos (with open) dentro de los métodos de alerta de producción, ya que hacían que las funciones devolvieran un valor vacío (None).

  * **Lo que modifique**
    * Modifiqué las clases de envío de alertas para que utilicen instrucciones return directas, permitiendo una validación robusta y limpia mediante assertions estrictos en pytest.
    * AnomalyDetector eliminando condicionales redundantes y modifiqué el archivo de pruebas test_fsm.py para corregir discrepancias de nombres entre métodos (.get_reading() en lugar de .read_temperature()) y sincronizar las etiquetas de contexto ([console] y [email]) generadas dinámicamente mediante metaprogramación.

  * **Resultados**
    * Tras las modificaciones en las firmas de los métodos y strings, se logró la ejecución exitosa de la suite con un estado final de PASSED.
------------------------------------------
  ## [16/07/2026] Semana 1 · Entrada 5
  # Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA
  
  **Contexto** Implementación y validación mediante pytest de los principios de diseño modular ISP y DIP aplicados a sistemas de adquisición de datos industriales.

  * **Pront enviado**
  >Solicitudes paso a paso para estructurar interfaces segregadas y diseñar un procesador de datos desacoplado mediante protocolos de inyección de dependencias, junto con la corrección de errores de sintaxis en la suite de pruebas.

  * **La IA propuso**
    * Una interfaz de sensor masiva ("gorda") que violaba el ISP y un acoplamiento directo a SQLServerRepository que violaba el DIP.
    * Plantillas automáticas con la instrucción super() y cadenas de texto en minúsculas para las validaciones de asserts del entorno.

  * **Lo que acepté**
    * La segregación de la interfaz gorda en múltiples contratos atómicos (Readable, Writable, Calibratable) usando Protocol.
    * La arquitectura de inversión de dependencias, permitiendo al DataProcessor operar sobre abstracciones de almacenamiento en lugar de bases de datos rígidas.

  * **Lo que rechace**
  * La generación automática de métodos basados en super().write() propuesta por el entorno, ya que provocaba llamadas vacías hacia métodos abstractos puros.

  * **Lo que modifique**
    * Modifiqué los argumentos y firmas en los métodos de prueba (añadiendo los paréntesis omitidos en la instanciación de las clases y corrigiendo operadores incorrectos como pipes | por puntos en la metaprogramación .__class__.__name__).
   * Sincronicé de manera estricta las etiquetas textuales (como "Calibracion exitosa" y "SQLServerRepository") respetando la coincidencia de mayúsculas y minúsculas para resolver fallos de aserción.

  * **Resultados**
   * Tras resolver los errores de importación y sintaxis (SyntaxError), la suite de la semana finalizó con estado exitoso en la terminal. 
--------------------------------

  ## [16/07/2026] Semana 1 · Entrada 6
  # Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA

  **Contexto** Transición de un driver de comunicación UART estructurado de sistemas embebidos en C hacia un módulo orientado a objetos moderno bajo los principios SOLID en Python.

  * **Pront enviado**
  > Solicitudes estructuradas para modelar configuraciones inmutables, implementar parsers polimórficos de protocolos (Modbus, NMEA, CAN), diseñar un dispositivo síncrono thread-safe y persistir telemetría en archivos JSON-lines.
   
  * **La IA propuso**
    * Estructuras de clases base para la configuración, decodificación y persistencia en disco de tramas UART.
    * Plantillas de firmas de métodos de prueba unitaria con docstrings detallados enfocados en aserciones de tipos de datos (`pytest.raises`).

  * **Lo que acepte**
    * La separación estricta de responsabilidades (SRP) dividiendo la adquisición, el almacenamiento y la configuración.
    * El uso de `dataclasses(frozen=True)` para forzar la inmutabilidad física de los parámetros de comunicación en el bus.
    * La extensión de distinción utilizando `threading.Lock` sobre un `deque` de tamaño fijo para simular un buffer circular de recepción thread-safe.

* **Lo que rechace**
    *  **Rechazado:** La estructura de la carpeta de pruebas inicial provista en formato singular (`test`), la cual fue renombrada a `tests` en plural para evitar fallos de autodescubrimiento en el motor de ejecución automática de `pytest`.

* **Lo que modifique**
    * Modifiqué el comportamiento del NMEAParser para añadir blindaje explícito usando  `errors='ignore'` durante la decodificación ASCII inicial, mitigando excepciones no controladas por ruido eléctrico en la telemetría simulada.
    * Ajusté los flujos lógicos en las pruebas de aserción del dispositivo UART para inyectar explícitamente tramas incompletas con DLCs erróneos, validando que el hardware lance excepciones deterministas y los logs generen trazas JSON válidas.

* **Resultado:** El módulo completo de comunicación UART compiló de manera limpia, alcanzando estado exitoso de PASSED en toda la suite experimental.
--------------------------------------
 ## [16/07/2026] Semana 1 · Entrada 6
  # Bitácora de Aprendizaje con Inteligencia Artificial - EDSIA
  * **Objetivos cumplidos**
    - Corrección y estandarización del tipado estático (`mypy`) en los módulos de principios SOLID y la FSM del semáforo.
    - Resolución de errores de arquitectura concurrente, firmas de retorno e indentación en las suites de prueba y producción.
    - Validación del pipeline de calidad local cumpliendo con los umbrales exigidos por la actividad.

  * **Pruebas y cobertura**
    1. **Pruebas y Cobertura:**
    `python -m pytest semana1/ -v --cov=semana1 --cov-report=term-missing`
    - **Resultado:** EXITOSO (PASSED). Cobertura final del **82%**, superando el mínimo del 70% requerido.
    2. **Linter de Estilo:**
    `ruff check semana1/`
    - **Resultado:** EXITOSO. Código 100% limpio de redundancias y advertencias de sintaxis.
    3. **Análisis de Tipado Estático:**
    `mypy semana1/ --ignore-missing-imports --explicit-package-bases`
    - **Resultado:** `Success: no issues found in 15 source files`.

  * **Leciones y aprendizaje**
    - Se corrigió un problema de indentación que anidaba las funciones de prueba de `pytest` dentro de la clase `TrafficLightFSM`, lo cual generaba conflictos con el argumento `self`. Los tests se extrajeron al nivel raíz del módulo.
    - Refactorización de las firmas de métodos en `AlertSender` y clases derivadas (`ConsoleAlertSender`, `EmailAlertSender`, `AnomalyDetector`) para coordinar el retorno de datos (`-> Optional[str]` / `-> str`) y el tipo de los parámetros (`threshold: float`), evitando comportamientos indeterminados y salidas `None` no declaradas.
    - Corrección de variables locales mal declaradas en el constructor de `ViolacionSRP`, transformándolas en atributos de instancia reales mediante `self.historial_guardado` para asegurar su persistencia en RAM.