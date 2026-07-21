# Product Backlog - Semana 2

## US-01: Refactorizar FSM del Semáforo al Patrón State
Como desarrollador de software embebido,
quiero refactorizar la máquina de estados del semáforo usando el patrón de diseño State,
para poder añadir nuevos estados (ej. Mantenimiento, Emergencia) sin modificar el núcleo de la FSM.

**Story Points:** 5 (Complejidad media, requiere reestructurar clases existentes y actualizar tests).

Scenario: Transición cíclica exitosa
  Given la FSM está inicializada en el estado "RedState"
  When se invoca el evento de transición regular
  Then la instancia de estado interno cambia a "GreenState"
  And el contador de ciclos del semáforo se incrementa

Scenario: Cambio a estado de emergencia
  Given la FSM operando en cualquier estado regular (Red, Green o Yellow)
  When el sistema recibe una interrupción de "Emergencia"
  Then la FSM cambia inmediatamente al estado "BlinkingYellowState"