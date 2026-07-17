import json
import logging
import threading
from collections import deque
from typing import List, Dict, Any, Optional
from semana1.uart_driver.config import UartConfig
from semana1.uart_driver.parsers import MenssageParser

# Configuración básica de un logger que genera salidas en formato string tipo JSON
logger = logging.getLogger("UartDevice")
handler = logging.StreamHandler()
formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class UartDevice:
    def __init__(self, config: UartConfig, parsers: List[MenssageParser], max_buffer_size: int = 64):
        """
        DIP: Inyectamos la configuración inmutable y la lista de parsers abstractos.
        """
        self.config = config
        self.parsers = parsers
        self.is_connected = False
        
        # Extensión: Buffer circular thread-safe utilizando deques y candados de exclusión
        self._buffer: deque = deque(maxlen=max_buffer_size)
        self._lock = threading.Lock()

    def _log_json(self, level: str, event: str, details: Dict[str, Any]) -> None:
        """Helper para estructurar logs como diccionarios serializables a JSON"""
        log_payload = {"event": event, **details}
        mensaje_json = json.dumps(log_payload)
        if level == "info":
            logger.info(mensaje_json)
        elif level == "error":
            logger.error(mensaje_json)

    def connect(self) -> None:
        if self.is_connected:
            return
        self.is_connected = True
        self._log_json("info", "uart_connected", {
            "baudrate": self.config.baudrate,
            "parity": self.config.parity,
            "stop_bits": self.config.stop_bits
        })

    def disconnect(self) -> None:
        if not self.is_connected:
            return
        self.is_connected = False
        self._log_json("info", "uart_disconnected", {"status": "success"})

    def simulate_hardware_interrupt(self, raw_bytes: bytes) -> None:
        """
        Simula una interrupción de hardware (ISR) que deposita bytes en el buffer circular.
        Operación estrictamente thread-safe.
        """
        with self._lock:
            for b in raw_bytes:
                self._buffer.append(b)

    def read_and_parse(self) -> Optional[Dict[str, Any]]:
        """
        Extrae los bytes almacenados en el buffer circular y busca un parser compatible.
        """
        if not self.is_connected:
            self._log_json("error", "read_failed", {"reason": "Device not connected"})
            raise RuntimeError("El dispositivo UART no está conectado.")

        # Extracción segura de datos desde el buffer circular
        with self._lock:
            if not self._buffer:
                return None
            data_to_parse = bytes(list(self._buffer))
            self._buffer.clear()

        # OCP / LSP: Recorremos los parsers inyectados polimórficamente
        for parser in self.parsers:
            if parser.can_parse(data_to_parse):
                try:
                    resultado = parser.parse(data_to_parse)
                    self._log_json("info", "parsing_success", {"protocol": resultado.get("protocolo")})
                    return resultado
                except ValueError as e:
                    self._log_json("error", "parsing_error", {"error": str(e)})
                    raise

        self._log_json("error", "unknown_protocol", {"raw_bytes": list(data_to_parse)})
        raise ValueError("Ninguno de los protocolos inyectados pudo parsear la trama de bytes.")