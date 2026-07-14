from enum import Enum, auto
from itertools import count

class TrafficLightState(Enum): #Aqui se nombra la clase heredada de Enum, que es una enumeración de estados posibles para un semáforo.
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class TrafficLightFSM:  ##Aqui se dice coimo empieza el semaforo de nuestra FSM.
    def __init__(self) -> None: #Iniciar las variables del semaforo
        self._state = TrafficLightState.RED #estado inicial del semaforo
        self._cycle_count = 0

    @property #Lo que hace property es leer de forma segura el estado en el quie debe de empezar el semaoforo.
    def state(self) -> TrafficLightState:
        return self._state

    def transition(self): #se usa transition para cmabiar los estados del semaforo.
        if self._state == TrafficLightState.RED:
            self._state = TrafficLightState.GREEN
        elif self._state == TrafficLightState.GREEN:
            self._state = TrafficLightState.YELLOW
        elif self._state == TrafficLightState.YELLOW:
            self._state = TrafficLightState.RED
        self._cycle_count += 1
        return self._state  #Regresa a el estado en el que se encuentra el semaforo.
    
    def test_full_cycle_returns_to_red():
        fsm = TrafficLightFSM()
    # 1. Llama a fsm.transition() 3 veces seguidas para dar la vuelta completa
        fsm.transition()
        fsm.transition()
        fsm.transition()
        assert fsm.state == TrafficLightState.RED  #Verifica que el estado del semaforo volvió a ser rojo después de un ciclo completo.
    # 2. Escribe un assert para verificar que fsm.state volvió a ser TrafficLightState.RED
    pass

    def test_cycle_counter_increments():
        fsm = TrafficLightFSM()
    # 1. Haz dos transiciones: fsm.transition() dos veces
        fsm.transition()
        fsm.transition()
    # 2. Escribe un assert para verificar que el contador interno es igual a 2
        assert fsm._cycle_count == 2
    # Pista: Accedes al contador con fsm._cycle_count
    pass
    