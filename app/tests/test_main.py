from fastapi.testclient import TestClient

from app.main import app

# Genebrar las señales
client = TestClient(app)

# Definimos un ID único para no chocar con las ya agregadas manualmente
TEST_SENSOR_ID = "ROBOT-01"


def test_crear_sensor() -> None:
    response = client.post(
        "/sensors",
        json={
            "id": TEST_SENSOR_ID,
            "type": "temperatura",
            "location": "Laboratorio QA",
        },
    )
    assert response.status_code in [
        201,
        409,
    ]  # 201 si es nuevo, 409 si ya existía de una prueba anterior


def test_listar_sensores() -> None:
    response = client.get("/sensors?limit=10&offset=0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_lectura_valida() -> None:
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings", json={"value": 25.5, "unit": "C"}
    )
    assert response.status_code == 201


# -----------------------------------------


def test_crear_lectura_fisica_invalida() -> None:
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings", json={"value": -300.0, "unit": "C"}
    )
    assert response.status_code == 422
    assert "Física inválida" in response.text


def test_crear_lectura_humedad_invalida() -> None:
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings", json={"value": 150.0, "unit": "%"}
    )
    assert response.status_code == 422


def test_sensor_duplicado_conflicto() -> None:
    response = client.post(
        "/sensors",
        json={
            "id": TEST_SENSOR_ID,
            "type": "temperatura",
            "location": "Laboratorio QA",
        },
    )
    assert response.status_code == 409


def test_listar_lecturas_sensor() -> None:
    response = client.get(f"/sensors/{TEST_SENSOR_ID}/readings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# -----------------------------------------
def test_obtener_sensor_no_existente() -> None:
    # Intenta leer un sensor fantasma (Cubre el Error 404 en GET)
    response = client.get("/sensors/FANTASMA-99")
    assert response.status_code == 404


def test_eliminar_sensor_no_existente() -> None:
    # Intenta borrar un sensor fantasma (Cubre el Error 404 en DELETE)
    response = client.delete("/sensors/FANTASMA-99")
    assert response.status_code == 404


def test_unidad_fisica_desconocida() -> None:
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings", json={"value": 10.0, "unit": "manzanas"}
    )
    assert response.status_code == 422
    assert "manzanas" in response.text


def test_eliminar_sensor() -> None:
    response = client.delete(f"/sensors/{TEST_SENSOR_ID}")
    assert response.status_code == 204


#------------------------------------------
def test_obtener_lectura_no_existente() -> None:
    response = client.get("/readings/99999")
    assert response.status_code == 404


def test_eliminar_lectura_no_existente() -> None:
    response = client.delete("/readings/99999")
    assert response.status_code == 404


def test_listar_lecturas_con_filtro_fechas() -> None: #Filtrar lecturas por fecha 
    url = f"/sensors/{TEST_SENSOR_ID}/readings?from=2026-01-01T00:00:00&to=2026-12-31T23:59:59"
    response = client.get(url)
    assert response.status_code == 200


def test_ruta_principal() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "API funcionando correctamente"}


def test_crear_lectura_presion_invalida() -> None:
    response = client.post(
        f"/sensors/{TEST_SENSOR_ID}/readings", 
        json={"value": 0.0, "unit": "HPA"}
    )
    # 422 Unprocessable Entity es el error que Pydantic lanza al fallar una validación
    assert response.status_code == 422
    assert "La presion atmosferica debe ser mayor a 0" in response.text

def test_listar_alertas_sensor() -> None:
    response = client.get("/sensors/ROBOT-01/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)