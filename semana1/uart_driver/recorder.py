import json
from typing import Dict, Any

class DataRecorder:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def record(self, data: Dict[str, Any]) -> None:
        """
        Guarda el diccionario de datos como una línea JSON (JSON-lines) en el archivo.
        Si el archivo no existe, lo crea; si existe, añade la línea al final.
        """
        if not isinstance(data, dict):
            raise TypeError("Los datos a registrar deben ser un diccionario.")
            
        # Convertimos el diccionario a un string JSON en una sola línea y añadimos salto de línea
        linea_json = json.dumps(data) + "\n"
        
        # Modo 'a' (append) para añadir datos al final sin borrar lo anterior
        with open(self.file_path, "a", encoding="utf-8") as f:
            f.write(linea_json)