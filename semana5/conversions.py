def fahrenheit_a_celsius(fahrenheit: float) -> float:
    """
    Convierte una temperatura de grados Fahrenheit a grados Celsius.

    Args:
        fahrenheit (float): La temperatura en grados Fahrenheit.

    Returns:
        float: La temperatura convertida a grados Celsius.

    Raises:
        TypeError: Si el valor de entrada no es un número (int o float).
    """
    if not isinstance(fahrenheit, (int, float)):
        raise TypeError("El valor de la temperatura debe ser numérico.")

    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 2)


# Prueba rápida del código
if __name__ == "__main__":
    try:
        print(f"98.6 F son {fahrenheit_a_celsius(98.6)} C")
        print(f"Texto F son {fahrenheit_a_celsius('noventa')} C")
    except TypeError as e:
        print(f"Error capturado exitosamente: {e}")
