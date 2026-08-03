# Usamos una versión ligera de Python 3.12
FROM python:3.12-slim

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# TRUCO DE CACHÉ: Copiamos dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de nuestro código
COPY . .

# Exponemos el puerto donde correrá FastAPI
EXPOSE 8000

# El comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]