import uuid

from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app
from app.models.alert import AlertModel  
from app.models.reading import ReadingModel  
from app.models.sensor import SensorModel  


Base.metadata.create_all(bind=engine)

client = TestClient(app)

client = TestClient(app)

TEST_SENSOR_ID = "ROBOT-01"

# ==========================================
# TESTS DE SENSORES
# ==========================================


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
    ]


def test_listar_sensores() -> None:
    response = client.get("/sensors?limit=10&offset=0")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


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


def test_obtener_sensor_no_existente() -> None:
    response = client.get("/sensors/FANTASMA-99")
    assert response.status_code == 404


def test_eliminar_sensor_no_existente() -> None:
    response = client.delete("/sensors/FANTASMA-99")
    assert response.status_code == 404


# ==========================================
# TESTS DE LECTURAS (CREACIÓN)
# ==========================================


def test_crear_lectura_valida() -> None:
    response = client.post("/readings/", json={"sensor_id": TEST_SENSOR_ID, "value": 25.5, "unit": "C"})

    print("\n--- ERROR DETALLADO ---")
    print(response.json())
    print("-----------------------")

    assert response.status_code == 201


def test_crear_lectura_fisica_invalida() -> None:
    response = client.post("/readings/", json={"sensor_id": TEST_SENSOR_ID, "value": -300.0, "unit": "C"})
    assert response.status_code == 422
    assert "Física inválida" in response.text


def test_crear_lectura_humedad_invalida() -> None:
    response = client.post("/readings/", json={"sensor_id": TEST_SENSOR_ID, "value": 150.0, "unit": "%"})
    assert response.status_code == 422


def test_unidad_fisica_desconocida() -> None:
    response = client.post("/readings/", json={"sensor_id": TEST_SENSOR_ID, "value": 10.0, "unit": "manzanas"})
    assert response.status_code == 422
    assert "manzanas" in response.text


def test_crear_lectura_presion_invalida() -> None:
    response = client.post("/readings/", json={"sensor_id": TEST_SENSOR_ID, "value": 0.0, "unit": "HPA"})
    assert response.status_code == 422
    assert "La presion atmosferica debe ser mayor a 0" in response.text


# ==========================================
# TESTS DE LECTURAS (BÚSQUEDA Y LISTADO)
# ==========================================


def test_listar_lecturas_sensor() -> None:
    response = client.get(f"/sensors/{TEST_SENSOR_ID}/readings")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_listar_lecturas_con_filtro_fechas() -> None:
    url = f"/sensors/{TEST_SENSOR_ID}/readings?from=2026-01-01T00:00:00&to=2026-12-31T23:59:59"
    response = client.get(url)
    assert response.status_code == 200


def test_obtener_lectura_no_existente() -> None:
    # Quitar la barra al final
    response = client.get("/readings/99999")
    assert response.status_code == 404


def test_eliminar_lectura_no_existente() -> None:
    # Quitar la barra al final
    response = client.delete("/readings/99999")
    assert response.status_code == 404


# ==========================================
# TESTS DE ALERTAS
# ==========================================


def test_listar_alertas_sensor() -> None:
    response = client.get(f"/sensors/{TEST_SENSOR_ID}/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ==========================================
# TESTS DE LIMPIEZA Y RUTAS PRINCIPALES
# ==========================================



def test_eliminar_sensor() -> None:
    id_unico = f"DEL-{uuid.uuid4().hex[:4]}"
    
    # 1. Intentamos crearlo
    res_post = client.post(
        "/sensors",
        json={
            "id": id_unico,
            "type": "temperatura",
            "location": "Laboratorio QA"
        }
    )
    assert res_post.status_code == 201, f"EXPLOTÓ EN EL POST: {res_post.json()}"
    
    res_del = client.delete(f"/sensors/{id_unico}")
    
    assert res_del.status_code == 204, f"EXPLOTÓ EN EL DELETE: {res_del.json()}"


def test_ruta_principal() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "API funcionando correctamente"}
