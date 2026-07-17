# UART Driver Modular con Arquitectura SOLID

Este módulo contiene la reimplementación de un controlador de comunicación UART para adquisición de datos embebidos. Transforma el paradigma clásico de firmware estructurado en C (basado en buffers globales compartidos y funciones acopladas) hacia una arquitectura orientada a objetos orientada a pruebas unitarias en Python moderno.

## Características Técnicas y Extensiones
- **Inmutabilidad de Hardware:** Configuración protegida contra corrupción en caliente mediante dataclasses congeladas.
- **Multitramado Concurrente:** Soporta decodificación simultánea de Modbus RTU, NMEA GPS y tramas CAN simplificadas.
- **Buffer Circular Thread-Safe:** Gestión de recepción asíncrona mediante `collections.deque` controlada por exclusión mutua (`threading.Lock`).
- **Telemetría Estructurada:** Sistema de logging nativo en formato JSON nativo y persistencia en disco optimizada mediante archivos JSON-lines (`.jsonl`).

## Requisitos e Instalación

1. Asegúrate de tener `pytest` instalado en tu entorno de desarrollo:
   ```bash
   pip install pytest
   - Comando para correrlo python -m pytest semana1/uart_driver/tests/ -v