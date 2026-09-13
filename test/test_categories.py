from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import categories_db

client = TestClient(app)

INITIAL_CATEGORIES = [
    {"id": 1, "name": "Computadores", "description": "Equipos de cómputo", "active": True},
    {"id": 2, "name": "Periféricos", "description": "Accesorios y periféricos", "active": False},
]


@pytest.fixture(autouse=True)
def reset_categories_db():
    # Antes de cada prueba, se restablece categories_db a su estado inicial
    # para que ninguna prueba dependa de lo que haya hecho otra (independencia).
    categories_db.clear()
    categories_db.extend([dict(category) for category in INITIAL_CATEGORIES])


# CA01 - Listar categorías
def test_listar_categorias():
    response = client.get("/categories")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


# CA02 - Consultar categoría existente
def test_consultar_categoria_existente():
    response = client.get("/categories/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Computadores"


# CA03 - Consultar categoría inexistente
def test_consultar_categoria_inexistente():
    response = client.get("/categories/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# CA04 - ID inválido
def test_id_invalido():
    response = client.get("/categories/abc")

    assert response.status_code == 422
    assert "detail" in response.json()


# CA05 - Crear categoría válida
def test_crear_categoria_valida():
    new_category = {
        "name": "Impresoras",
        "description": "Impresoras y consumibles",
        "active": True,
    }

    response = client.post("/categories", json=new_category)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_category["name"]
    assert data["description"] == new_category["description"]
    assert data["active"] is True
    assert "id" in data


# CA06 - Nombre demasiado corto
def test_nombre_demasiado_corto():
    new_category = {"name": "PC", "description": "Nombre muy corto"}

    response = client.post("/categories", json=new_category)

    assert response.status_code == 422
    assert "detail" in response.json()


# CA07 - Falta el nombre
def test_falta_nombre():
    new_category = {"description": "Categoría sin nombre"}

    response = client.post("/categories", json=new_category)

    assert response.status_code == 422
    assert "detail" in response.json()


# CA08 - Actualizar categoría existente
def test_actualizar_categoria_existente():
    response = client.patch("/categories/1", json={"description": "Nueva descripción"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["description"] == "Nueva descripción"
    # El nombre no se envió en el PATCH y debe permanecer sin cambios
    assert data["name"] == "Computadores"


# CA09 - Actualizar categoría inexistente
def test_actualizar_categoria_inexistente():
    response = client.patch("/categories/999", json={"description": "No existe"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# CA10 - Eliminar categoría existente
def test_eliminar_categoria_existente():
    response = client.delete("/categories/1")

    assert response.status_code == 204
    assert response.content == b""

    # Verificar que ya no existe
    get_response = client.get("/categories/1")
    assert get_response.status_code == 404


# CA11 - Eliminar categoría inexistente
def test_eliminar_categoria_inexistente():
    response = client.delete("/categories/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# CA12 - Filtrar categorías activas
def test_filtrar_categorias_activas():
    response = client.get("/categories?active=true")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert all(category["active"] is True for category in data)


# Reto opcional - Búsqueda por nombre (case-insensitive)
def test_buscar_por_nombre_encuentra_resultado():
    response = client.get("/categories?search=comp")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Computadores"


def test_buscar_por_nombre_sin_resultados():
    response = client.get("/categories?search=xyz")

    assert response.status_code == 200
    assert response.json() == []
