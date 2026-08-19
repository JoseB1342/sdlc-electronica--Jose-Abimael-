# ADR 0001: Uso de FastAPI como framework web

## Estado
Aceptado

## Contexto
El proyecto SensorHub requiere una API capaz de recibir lecturas de hardware IoT y consultar datos rápidamente. Necesitábamos un framework moderno, rápido y que facilitara la validación de datos (tipado estricto) para evitar errores comunes en la ingesta de telemetría.

## Decisión
Decidimos utilizar **FastAPI** en lugar de alternativas como Flask o Django. 

## Consecuencias
* **Positivas:** La validación de datos viene gratis gracias a Pydantic. La documentación automática (Swagger UI) nos ahorró horas de escribir docs a mano. El rendimiento es excepcionalmente alto.
* **Negativas:** La curva de aprendizaje inicial con operaciones asíncronas e inyección de dependencias fue un poco más empinada.