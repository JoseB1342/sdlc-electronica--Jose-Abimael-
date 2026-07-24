# Arquitectura del Sistema IoT (C4 - Nivel 2: Contenedores)
Person(admin, "Supervisor de Bodega", "Monitorea alertas e historial")
  
  System_Boundary(iot_system, "Sistema Central IoT (Python)") {
    Container(simulator, "Sensor Simulator", "Python", "Genera lecturas con distribución Gaussiana")
    Container(detector, "Anomaly Detector", "Python", "Evalúa umbrales inyectados")
    Container(alert_mgr, "Alert Manager", "Python", "Despacha eventos usando Patrón Strategy")
  }

  System_Ext(console, "Terminal/Consola", "Salida estándar (STDOUT)")
  System_Ext(file_sys, "Sistema de Archivos", "Archivos de log (.log)")

  Rel(simulator, detector, "Envía SensorReading", "Llamada a función")
  Rel(detector, alert_mgr, "Dispara eventos de anomalía", "Llamada a función")
  Rel(alert_mgr, console, "Imprime usando ConsoleStrategy", "I/O")
  Rel(alert_mgr, file_sys, "Guarda usando FileStrategy", "I/O")
  Rel(admin, console, "Observa las alertas")