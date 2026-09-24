# ═══════════════════════════════════════════════════════════════
# Pruebas automatizadas · CATEGORÍAS  (RF01–RF04, RN01–RN02)
# Cada test lleva su ID de caso → requisito (trazabilidad con docs/).
# Estructura: Arrange (datos) → Act (petición) → Assert (esperado).
# "EXTRA" = no está en casos-prueba.md (fuera del contrato o refuerzo).
# ═══════════════════════════════════════════════════════════════
import pytest
from fastapi.testclient import TestClient

from app.database import categories_db, products_db
from app.main import app

# TestClient simula peticiones HTTP sin levantar el servidor.
client = TestClient(app)
INITIAL_CATEGORIES = [
    {"id": 1, "name": "Periféricos"},
    {"id": 2, "name": "Audio"},
]
INITIAL_PRODUCTS = [
    {"id": 1, "name": "Mouse inalámbrico", "price": 120000.0, "stock": 5, "category_id": 1},
    {"id": 2, "name": "Monitor", "price": 850000.0, "stock": 0, "category_id": 1},
]


# autouse → se ejecuta antes de CADA test: datos siempre iguales, pruebas
# independientes (el orden no importa). "[:] =" modifica la lista EN SITIO;
# reasignarla rompería la referencia que usa main.py.
@pytest.fixture(autouse=True)
def reset_db():
    categories_db[:] = [dict(item) for item in INITIAL_CATEGORIES]
    products_db[:] = [dict(item) for item in INITIAL_PRODUCTS]


# CP-CAT-02 · RF02 · Positiva → 200 y lista con las 2 categorías base.
def test_list_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) == 2


# CP-CAT-03 · RF03 · Positiva → 200 y datos de la categoría 1.
def test_get_existing_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Periféricos"


# CP-CAT-04 · RF04 · Negativa · Recurso inexistente → 404 (valida código y mensaje).
def test_get_missing_category_returns_404():
    response = client.get("/categories/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# EXTRA · id no numérico ("abc"): FastAPI rechaza el tipo de la ruta → 422.
def test_get_invalid_category_id_returns_422():
    assert client.get("/categories/abc").status_code == 422


# CP-CAT-01 · RF01 · Positiva → 201 y objeto creado.
# Usa "Computadores": "Periféricos" ya existe en los datos base (daría 409).
def test_create_category_valid():
    response = client.post("/categories", json={"name": "Computadores"})
    assert response.status_code == 201
    assert response.json()["name"] == "Computadores"


# CP-CAT-05 · RN01 · Frontera negativa → 2 caracteres ("AB") = 422.
def test_category_name_shorter_than_three_returns_422():
    assert client.post("/categories", json={"name": "AB"}).status_code == 422


# CP-CAT-06 · RN01 · Frontera positiva → 3 caracteres ("Red") = 201 (límite inferior válido).
def test_category_name_exactly_three_characters_is_valid():
    assert client.post("/categories", json={"name": "Red"}).status_code == 201


# EXTRA · RN01 "obligatorio": cuerpo sin el campo name → 422.
def test_category_name_missing_returns_422():
    assert client.post("/categories", json={}).status_code == 422


# CP-CAT-08 · RN02 · Negativa → "audio" ya existe como "Audio" → 409 (case-insensitive).
def test_duplicate_category_name_is_case_insensitive():
    response = client.post("/categories", json={"name": "audio"})
    assert response.status_code == 409
    assert response.json() == {"detail": "Category name already exists"}


# CP-CAT-07 · RN01 · Frontera positiva → 60 caracteres = 201 (límite superior válido).
def test_category_name_length_sixty_is_valid():
    response = client.post("/categories", json={"name": "A" * 60})
    assert response.status_code == 201


# EXTRA · RN01 · Frontera negativa → 61 caracteres = 422 (complementa CP-CAT-07).
def test_category_name_length_sixty_one_returns_422():
    assert client.post("/categories", json={"name": "A" * 61}).status_code == 422


# EXTRA (PATCH, fuera del contrato) → cambia el nombre y responde 200.
def test_update_category_name():
    response = client.patch("/categories/1", json={"name": "Periferia"})
    assert response.status_code == 200
    assert response.json()["name"] == "Periferia"


# EXTRA (PATCH) · RN02 también aplica al actualizar → 409.
def test_update_category_duplicate_returns_409():
    assert client.patch("/categories/1", json={"name": "audio"}).status_code == 409


# EXTRA (DELETE categoría, fuera del contrato) → 204 y cuerpo vacío.
def test_delete_category_returns_204_without_body():
    response = client.delete("/categories/1")
    assert response.status_code == 204
    assert response.content == b""
