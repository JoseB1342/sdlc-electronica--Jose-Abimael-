import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from app.db import SessionLocal
from app.models.reading import ReadingModel

# --- CONFIGURACIÓN DEL BROKER PÚBLICO ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "joseb/sensorhub/telemetry"

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"✅ Conectado a MQTT Broker Público: {MQTT_BROKER}")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"❌ Error al conectar a MQTT. Código: {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"📩 ¡Mensaje atrapado desde Wokwi!: {payload}")
        
        sensor_id = payload.get("sensor_id")
        value = payload.get("value")
        
        if sensor_id and value is not None:
            db = SessionLocal()
            try:
                nueva_lectura = ReadingModel(sensor_id=sensor_id, value=value, unit="raw") 
                db.add(nueva_lectura)
                db.commit()
                print(f"💾 Guardado en BD: Sensor {sensor_id} -> {value}")
            except Exception as e:
                db.rollback()
                print(f"⚠️ Error guardando en BD (¿Existe el sensor en tu base de datos?): {e}")
            finally:
                db.close()
                
    except json.JSONDecodeError:
        print("⚠️ El mensaje recibido no es un JSON válido")

def start_mqtt_client():
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        print("Iniciando cliente MQTT en segundo plano...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start() 
    except Exception as e:
        print(f"❌ No se pudo iniciar el cliente MQTT: {e}")