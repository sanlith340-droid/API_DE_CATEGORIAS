# ═══════════════════════════════════════════════════════════════
# Pruebas automatizadas · PRODUCTOS  (RF05–RF12, RN03–RN08)
# Cada test lleva su ID de caso → requisito (trazabilidad con docs/).
# Estructura: Arrange (datos) → Act (petición) → Assert (esperado).
# "EXTRA" = no está en casos-prueba.md (fuera del contrato).
# ═══════════════════════════════════════════════════════════════
import pytest
from fastapi.testclient import TestClient

from app.database import categories_db, products_db
from app.main import app

client = TestClient(app)

INITIAL_CATEGORIES = [
    {"id": 1, "name": "Periféricos"},
    {"id": 2, "name": "Audio"},
]
INITIAL_PRODUCTS = [
    {"id": 1, "name": "Mouse inalámbrico", "price": 120000.0, "stock": 5, "category_id": 1},
    {"id": 2, "name": "Monitor", "price": 850000.0, "stock": 0, "category_id": 1},
]


# autouse → datos base idénticos antes de CADA test (pruebas independientes).
@pytest.fixture(autouse=True)
def reset_db():
    categories_db[:] = [dict(item) for item in INITIAL_CATEGORIES]
    products_db[:] = [dict(item) for item in INITIAL_PRODUCTS]


# Producto válido por defecto. Cada test cambia SOLO el campo que prueba:
# si falla, se sabe exactamente qué dato lo causó.
def valid_product(**overrides):
    data = {"name": "Teclado mecánico", "price": 250000, "stock": 10, "category_id": 1}
    data.update(overrides)
    return data


# ── Positivas: RF05–RF07 ────────────────────────────────────────

# CP-PROD-02 · RF06 · Positiva → 200 y los 2 productos base.
def test_list_products_returns_200():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


# CP-PROD-01 · RF05 · Positiva → 201 y producto asociado a la categoría 1.
def test_create_product_valid():
    response = client.post("/products", json=valid_product())
    assert response.status_code == 201
    assert response.json()["category_id"] == 1


# CP-PROD-03 · RF07 · Positiva → 200 y datos del producto 1.
def test_get_existing_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse inalámbrico"


# CP-PROD-04 · RF08 · Negativa · Recurso inexistente → 404.
def test_get_missing_product_returns_404():
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


# ── Validaciones al crear: RN03–RN06 ────────────────────────────

# CP-PROD-09 · RN03 · Frontera negativa → nombre de 2 caracteres = 422.
def test_create_product_name_too_short_returns_422():
    assert client.post("/products", json=valid_product(name="AB")).status_code == 422


# CP-PROD-10 · RN03 · Frontera positiva → nombre de 3 caracteres ("RAM") = 201.
def test_create_product_name_exactly_three_characters_is_valid():
    assert client.post("/products", json=valid_product(name="RAM")).status_code == 201


# CP-PROD-11 · RN04 · Frontera negativa → precio 0 = 422 (debe ser ESTRICTAMENTE > 0).
def test_create_product_price_zero_returns_422():
    assert client.post("/products", json=valid_product(price=0)).status_code == 422


# CP-PROD-12 · RN04 · Negativa → precio -1000 = 422.
def test_create_product_negative_price_returns_422():
    assert client.post("/products", json=valid_product(price=-1000)).status_code == 422


# CP-PROD-13 · RN04 · Frontera positiva → precio mínimo válido 0.01 = 201.
def test_create_product_minimum_positive_price_is_valid():
    assert client.post("/products", json=valid_product(price=0.01)).status_code == 201


# CP-PROD-14 · RN05/RN07 · Frontera positiva → stock 0 se ACEPTA (201).
def test_create_product_stock_zero_is_valid():
    assert client.post("/products", json=valid_product(stock=0)).status_code == 201


# CP-PROD-15 · RN05 · Negativa → stock -1 = 422.
def test_create_product_negative_stock_returns_422():
    assert client.post("/products", json=valid_product(stock=-1)).status_code == 422


# CP-PROD-16 · RN06 · Negativa → categoría inexistente = 404 (no 422: es regla de negocio).
def test_create_product_missing_category_returns_404():
    response = client.post("/products", json=valid_product(category_id=99999))
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


# ── Actualización (PUT): RF09, RF10, RN08 ───────────────────────

# CP-PROD-05 · RF09 · Positiva → 200; verifica que los cambios se aplicaron.
def test_put_product_valid():
    replacement = valid_product(name="Monitor 4K", price=900000, stock=3, category_id=2)
    response = client.put("/products/1", json=replacement)
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor 4K"
    assert response.json()["category_id"] == 2


# CP-PROD-06 · RF10 · Negativa · Recurso inexistente → 404 (cuerpo válido, id 99999).
def test_put_missing_product_returns_404():
    response = client.put("/products/99999", json=valid_product())
    assert response.status_code == 404


# CP-PROD-17 · RN08 · Negativa → al actualizar también se rechaza precio 0 (422).
def test_put_product_invalid_price_returns_422():
    assert client.put("/products/1", json=valid_product(price=0)).status_code == 422


# CP-PROD-18 · RN08/RN06 · Negativa → al actualizar, categoría inexistente = 404.
def test_put_product_invalid_category_returns_404():
    assert client.put("/products/1", json=valid_product(category_id=99999)).status_code == 404


# EXTRA (PATCH, fuera del contrato) → actualiza solo el precio.
def test_patch_product_price():
    response = client.patch("/products/1", json={"price": 300000})
    assert response.status_code == 200
    assert response.json()["price"] == 300000


# ── Eliminación: RF11, RF12 ─────────────────────────────────────

# CP-PROD-07 · RF11 · Positiva → 204 sin cuerpo y luego GET da 404 (ya no existe).
def test_delete_product_returns_204_without_body():
    response = client.delete("/products/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/products/1").status_code == 404


# CP-PROD-08 · RF12 · Negativa · Recurso inexistente → 404.
def test_delete_missing_product_returns_404():
    assert client.delete("/products/99999").status_code == 404


# ── Extras (filtros fuera del contrato) ─────────────────────────

# EXTRA · filtro ?category_id=1 solo devuelve productos de esa categoría.
def test_filter_products_by_category_id():
    response = client.get("/products", params={"category_id": 1})
    assert response.status_code == 200
    assert all(item["category_id"] == 1 for item in response.json())


# EXTRA · búsqueda ?search=mouse sin distinguir mayúsculas → 1 resultado.
def test_search_products_by_name():
    response = client.get("/products", params={"search": "mouse"})
    assert response.status_code == 200
    assert len(response.json()) == 1
