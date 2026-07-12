from semana0.hola_sensor import Sensor


def test_sensor_read_returns_correct_value():
    # 1. Preparar (Instanciar nuestra clase Sensor)
    sensor_objeto = Sensor()

    # 2. Actuar (Llamar al método read)
    resultado = sensor_objeto.read()

    # 3. Afirmar (Verificar que el resultado sea exactamente 23.5)
    assert resultado == 23.5