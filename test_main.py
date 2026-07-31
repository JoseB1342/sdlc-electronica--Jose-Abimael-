from fastapi.testclient import TestClient
from app.main import app

# Genebrar las señales
client = TestClient(app)

# Definimos un ID único para no chocar con las ya agregadas manualmente
TEST_SENSOR_ID = "ROBOT-01"

def test_crear_sensor():
    response = client.post(
        "/sensors",
        json={"id": TEST_SENSOR_ID, "type": "temperatura", "location": "Laboratorio QA"}
    )
    assert response.status_code in [201, 409] # 201 si es nuevo, 409 si ya existía de una prueba anterior

def test_listar_sensores():
    response = client.get("/sensors?limit=10&offset=0")
    assert response.status_code == 200
    assert type(response.json()) == list

def test_crear_lectura_valida():
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings",
        json={"value": 25.5, "unit": "C"}
    )
    assert response.status_code == 201

#-----------------------------------------

def test_crear_lectura_fisica_invalida():
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings",
        json={"value": -300.0, "unit": "C"}
    )
    assert response.status_code == 422
    assert "Física inválida" in response.text

def test_crear_lectura_humedad_invalida():
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings",
        json={"value": 150.0, "unit": "%"}
    )
    assert response.status_code == 422

def test_sensor_duplicado_conflicto():
    response = client.post(
        "/sensors",
        json={"id": TEST_SENSOR_ID, "type": "temperatura", "location": "Laboratorio QA"}
    )
    assert response.status_code == 409

def test_listar_lecturas_sensor():
    response = client.get(f"/sensors/{TEST_SENSOR_ID}/readings")
    assert response.status_code == 200
    assert type(response.json()) == list

#-----------------------------------------
def test_obtener_sensor_no_existente():
    # Intenta leer un sensor fantasma (Cubre el Error 404 en GET)
    response = client.get("/sensors/FANTASMA-99")
    assert response.status_code == 404

def test_eliminar_sensor_no_existente():
    # Intenta borrar un sensor fantasma (Cubre el Error 404 en DELETE)
    response = client.delete("/sensors/FANTASMA-99")
    assert response.status_code == 404

def test_unidad_fisica_desconocida():
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings",
        json={"value": 10.0, "unit": "manzanas"}
    )
    assert response.status_code == 422
    assert "manzanas" in response.text

    
def test_eliminar_sensor():
    response = client.delete(f"/sensors/{TEST_SENSOR_ID}")
    assert response.status_code == 204