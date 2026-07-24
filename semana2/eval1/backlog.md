# Product Backlog - Sistema de Monitoreo IoT

## US-01: Registrar lectura de sensor (SensorReading)
**Prioridad:** Must Have | **Story Points:** 3
Como sistema de recolección de datos,
quiero registrar la lectura de temperatura y humedad de un sensor con su timestamp,
para mantener un registro inmutable del estado ambiental de la bodega.

**Scenario: Lectura ambiental válida**
  Given un sensor activo reportando datos
  When recibe una lectura de 25.0 °C y 50% de humedad
  Then se crea un objeto SensorReading inmutable
  And el timestamp se asigna automáticamente al momento actual

## US-02: Detección de anomalías (AnomalyDetector)
**Prioridad:** Must Have | **Story Points:** 5
Como supervisor de la bodega,
quiero que el sistema evalúe las lecturas contra umbrales inyectados,
para detectar si la temperatura o la humedad superan los límites permitidos.

**Scenario: Detección de temperatura crítica**
  Given un AnomalyDetector configurado con umbral máximo de 35.0 °C
  When evalúa un SensorReading de 36.5 °C
  Then el detector retorna verdadero (anomalía detectada)
  And clasifica la alerta por alta temperatura

**Scenario: Lectura dentro de los parámetros normales**
  Given un AnomalyDetector configurado con umbrales estándar
  When evalúa un SensorReading de 28.0 °C y 60% de humedad
  Then el detector retorna falso (sin anomalía)

## US-03: Despachador de Alertas (AlertManager)
**Prioridad:** Must Have | **Story Points:** 8
Como arquitecto de software,
quiero que el sistema de alertas utilice el Patrón Strategy (abstracción),
para poder enviar notificaciones a diferentes medios sin modificar la lógica central.

**Scenario: Enviar alerta a múltiples canales**
  Given un AlertManager configurado con dos estrategias de salida
  When recibe una alerta de anomalía
  Then despacha la alerta a ambas estrategias de forma independiente

## US-04: Estrategia de Alerta por Consola
**Prioridad:** Must Have | **Story Points:** 2
Como desarrollador en fase de pruebas,
quiero una estrategia de alerta que imprima en la consola estándar,
para verificar rápidamente que el sistema detecta anomalías en tiempo real.

**Scenario: Imprimir alerta en consola**
  Given la estrategia ConsoleAlertStrategy
  When recibe una alerta de humedad del "Sensor-03"
  Then imprime un mensaje formateado con la fecha, sensor y valores en la salida estándar

## US-05: Estrategia de Alerta en Archivo
**Prioridad:** Should Have | **Story Points:** 3
Como auditor de calidad,
quiero que las alertas se guarden en un archivo de texto plano (.log),
para tener un registro auditable en caso de que el sistema se reinicie.

**Scenario: Escribir alerta en archivo de log**
  Given la estrategia FileAlertStrategy apuntando a "alertas.log"
  When recibe una alerta de temperatura
  Then añade (append) la información de la alerta como una nueva línea en el archivo

## US-06: Simulador de Sensores con Distribución Gaussiana
**Prioridad:** Should Have | **Story Points:** 5
Como ingeniero de pruebas,
quiero un simulador que genere datos de temperatura y humedad usando una distribución normal (Gaussiana),
para probar el sistema con datos realistas en lugar de valores fijos.

**Scenario: Generación de valores realistas**
  Given un SensorSimulator configurado con media de 25 °C y desviación de 2.0
  When se solicita una nueva lectura
  Then retorna un valor que estadísticamente pertenece a esa campana de Gauss

## US-07: Ciclos de Monitoreo 
**Prioridad:** Should Have | **Story Points:** 5
Como operador de planta,
quiero que el sistema consulte los 10 sensores de forma automática cada 30 segundos,
para no tener que iniciar el chequeo manualmente.

**Scenario: Ciclo completo de recolección**
  Given una red con 10 sensores registrados
  When el orquestador inicia un ciclo de recolección
  Then obtiene exactamente 10 lecturas
  And las pasa al detector de anomalías automáticamente

## US-08: Detección de Sensores Desconectados 
**Prioridad:** Could Have | **Story Points:** 5
Como equipo de mantenimiento,
quiero que el sistema genere una alerta si un sensor no reporta datos en 3 ciclos seguidos,
para identificar hardware dañado o baterías agotadas.

**Scenario: Sensor fuera de línea**
  Given un sensor que falló sus últimas 3 lecturas
  When el sistema evalúa el estado de la red
  Then emite una alerta

## US-09: Dashboard de Métricas Históricas
**Prioridad:** Could Have | **Story Points:** 13
Como gerente de planta,
quiero una interfaz que muestre el promedio de temperatura de las últimas 24 horas,
para identificar zonas de la bodega que requieran mejor ventilación.

**Scenario: Consulta de promedios**
  Given una base de datos con lecturas de 1 día completo
  When el usuario solicita el promedio del "Sensor-05"
  Then el sistema calcula y retorna la media matemática de esos registros

## US-10: Notificaciones por SMS 
**Prioridad:** Won't Have  | **Story Points:** 8
Como supervisor de guardia,
quiero recibir alertas críticas por mensaje de texto a mi celular,
para reaccionar inmediatamente aunque no esté frente a la computadora.

**Scenario: Envío de SMS crítico**
  Given la estrategia SMSAlertStrategy configurada con credenciales de API
  When ocurre una alerta de temperatura > 40 °C
  Then invoca la API externa y retorna un código de éxito 200