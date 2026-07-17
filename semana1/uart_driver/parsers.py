from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class MenssageParser(ABC):
    @abstractmethod
    def can_parse(self, data: bytes) -> bool:
        """
        Evalúa si la trama de bytes corresponde a este protocolo específico.
        """
        pass

    @abstractmethod
    def parse(self,data: bytes) -> Dict[str, Any]:
        """
        Decodifica la trama cruda y devuelve un diccionario con los datos estructurados.
        Levanta ValueError si la trama está corrupta.
        """
        pass

class ModbusParser(MenssageParser):
    def can_parse(self, data:bytes) -> bool:
        return len(data) >= 4 and data[0] in [0x01, 0x02, 0x03]
    
    def parse(self, data: bytes) ->Dict[str, Any]:
        if not self.can_parse(data):
            raise ValueError("Trama invalida por el protocolo Modbus RTU.")

        slave_id = data[0]
        function_code = data[1]

        return {
            "protocolo": "Modbus_RTU",
            "slave_id": slave_id,
            "function_code": function_code,
            "payload_len": len(data) - 2
        }
    
class NMEAParser(MenssageParser):
     def can_parse(self, data: bytes) -> bool:
        try:
                texto = data.decode("ascii", errors="ignore")
                return texto.startswith("$GPGGA")
        except Exception:
            return False 
            
     def parse (self, data:  bytes) ->Dict[str, Any]:
        if not self.can_parse(data):
         raise ValueError("Trama invalida para el protocolo NMEA GPS.")
        
        try:
            texto = data.decode("ascii").strip()
            partes = texto.split(",")

            return {
                "protocolo": "NMEA_GPS",
                "sentence": partes[0],
                "time": partes[1] if len(partes) > 1 else "",
                "latitud": float(partes[2]) if len(partes) > 2 and partes[2] else 0.0,
                "longitud": float(partes[4]) if len(partes) > 4 and partes[4] else 0.0
            }
        except Exception as e:
            raise ValueError(f"Error parseando sentencia NMEA corrupta: {str(e)}")
        
class CanSimplificadoParser(MenssageParser):
    """
    Extensión de Distinción: Parser para tramas CAN encapsuladas en UART
    Estructura esperada: [ID_MSB, ID_LSB, DLC, DATA_0, ... DATA_N]
    """
    def can_parse(self, data: bytes) -> bool:
        return len(data) >= 3 and  data[2] <=8
    
    def parse(self, data: bytes) -> Dict[str, Any]:
        if not self.can_parse(data):
            raise  ValueError("Trama invalida para protocolo can simplificado")
        
        can_id = (data[0]<<8) | data [1]
        dlc = data[2]

        if len(data) < 3 + dlc:
            raise ValueError("La longitud de la trama no coincide con el DLC especifico")
        
        payload = list(data[3:3+dlc])

        return {
            "protocolo": "CAN_Simplificado",
            "can_id": hex(can_id),
            "dlc": dlc,
            "payload": payload
        }
