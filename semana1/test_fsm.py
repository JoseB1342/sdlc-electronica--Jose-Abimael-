import pytest
# Aquí le decimos a Python que vaya a tu archivo fsm_demo y traiga el semáforo
from semana1.fsm_demo import TrafficLightFSM, TrafficLightState

def test_initial_state():
    fsm = TrafficLightFSM()
    assert fsm.state == TrafficLightState.RED

def test_transition_red_to_green():
    fsm = TrafficLightFSM()
    fsm.transition()
    assert fsm.state == TrafficLightState.GREEN

def test_full_cycle_returns_to_red():
    fsm = TrafficLightFSM()
    # Damos la vuelta completa
    fsm.transition()  # Pasa a GREEN
    fsm.transition()  # Pasa a YELLOW
    fsm.transition()  # Pasa a RED
    
    # Comprobamos que regresó al inicio
    assert fsm.state == TrafficLightState.RED

def test_cycle_counter_increments():
    fsm = TrafficLightFSM()
    fsm.transition()  # Primer transición
    fsm.transition()  # Segunda transición
    
    # Comprobamos que el contador interno es 2
    assert fsm._cycle_count == 2
    