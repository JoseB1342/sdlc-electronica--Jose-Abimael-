from enum import Enum, auto

class TrafficLightState(Enum): # Aqui se nombra la clase heredada de Enum, que es una enumeración de estados posibles para un semáforo.
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class TrafficLightFSM:  ## Aqui se dice coimo empieza el semaforo de nuestra FSM.
    def __init__(self) -> None: # Iniciar las variables del semaforo
        self._state = TrafficLightState.RED # estado inicial del semaforo
        self._cycle_count = 0

    @property # Lo que hace property es leer de forma segura el estado en el quie debe de empezar el semaoforo.
    def state(self) -> TrafficLightState:
        return self._state

    # CORRECCIÓN: Se agrega self (que ya lo tenías) y se especifica el tipo de retorno '-> TrafficLightState' para mypy
    def transition(self) -> TrafficLightState: # se usa transition para cmabiar los estados del semaforo.
        if self._state == TrafficLightState.RED:
            self._state = TrafficLightState.GREEN
        elif self._state == TrafficLightState.GREEN:
            self._state = TrafficLightState.YELLOW
        elif self._state == TrafficLightState.YELLOW:
            self._state = TrafficLightState.RED
        self._cycle_count += 1
        return self._state  # Regresa a el estado en el que se encuentra el semaforo.
    

# CORRECCIÓN: Sacamos las funciones de prueba fuera de la clase TrafficLightFSM (eliminando la indentación de 4 espacios)
# Además, les agregamos el tipo de retorno '-> None' que exige mypy para funciones de prueba.

def test_full_cycle_returns_to_red() -> None:
    fsm = TrafficLightFSM()
    # 1. Llama a fsm.transition() 3 veces seguidas para dar la vuelta completa
    fsm.transition()
    fsm.transition()
    fsm.transition()
    assert fsm.state == TrafficLightState.RED  # Verifica que el estado del semaforo volvió a ser rojo después de un ciclo completo.

def test_cycle_counter_increments() -> None:
    fsm = TrafficLightFSM()
    # 1. Haz dos transiciones: fsm.transition() dos veces
    fsm.transition()
    fsm.transition()
    # 2. Escribe un assert para verificar que el contador interno es igual a 2
    assert fsm._cycle_count == 2