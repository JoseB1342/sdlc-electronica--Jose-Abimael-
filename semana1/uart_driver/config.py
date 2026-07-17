from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class UartConfig:
    baudrate: int
    parity: Literal["N","E","O"] #None, Even, Odd
    stop_bits: Literal[1,2]
    timeout: float

    def __post_init__(self)->None:
        """
        Validación posterior a la inicialización.
        Garantiza que no se creen configuraciones con parámetros de hardware inválidos.
        """
        baudrates_validos = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]

        if self.baudrate not in baudrates_validos:
            raise ValueError(f"Baudrate {self.baudrate} no es válido para este controlador UART.") 
        
        if self.timeout < 0:
            raise ValueError("El timeout no puede ser valor negativo")