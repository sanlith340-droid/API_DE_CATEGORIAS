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


@pytest.fixture(autouse=True)
def reset_db():
    categories_db[:] = [dict(item) for item in INITIAL_CATEGORIES]
    products_db[:] = [dict(item) for item in INITIAL_PRODUCTS]


def valid_product(**overrides):
    data = {"name": "Teclado mecánico", "price": 250000, "stock": 10, "category_id": 1}
    data.update(overrides)
    return data


def test_list_products_returns_200():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_create_product_valid():
    response = client.post("/products", json=valid_product())
    assert response.status_code == 201
    assert response.json()["category_id"] == 1


def test_get_existing_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Mouse inalámbrico"


def test_get_missing_product_returns_404():
    response = client.get("/products/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product_name_too_short_returns_422():
    assert client.post("/products", json=valid_product(name="AB")).status_code == 422


def test_create_product_name_exactly_three_characters_is_valid():
    assert client.post("/products", json=valid_product(name="RAM")).status_code == 201


def test_create_product_price_zero_returns_422():
    assert client.post("/products", json=valid_product(price=0)).status_code == 422


def test_create_product_negative_price_returns_422():
    assert client.post("/products", json=valid_product(price=-1000)).status_code == 422


def test_create_product_minimum_positive_price_is_valid():
    assert client.post("/products", json=valid_product(price=0.01)).status_code == 201


def test_create_product_stock_zero_is_valid():
    assert client.post("/products", json=valid_product(stock=0)).status_code == 201


def test_create_product_negative_stock_returns_422():
    assert client.post("/products", json=valid_product(stock=-1)).status_code == 422


def test_create_product_missing_category_returns_404():
    response = client.post("/products", json=valid_product(category_id=99999))
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_put_product_valid():
    replacement = valid_product(name="Monitor 4K", price=900000, stock=3, category_id=2)
    response = client.put("/products/1", json=replacement)
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor 4K"
    assert response.json()["category_id"] == 2


def test_put_missing_product_returns_404():
    response = client.put("/products/99999", json=valid_product())
    assert response.status_code == 404


def test_put_product_invalid_price_returns_422():
    assert client.put("/products/1", json=valid_product(price=0)).status_code == 422


def test_put_product_invalid_category_returns_404():
    assert client.put("/products/1", json=valid_product(category_id=99999)).status_code == 404


def test_patch_product_price():
    response = client.patch("/products/1", json={"price": 300000})
    assert response.status_code == 200
    assert response.json()["price"] == 300000


def test_delete_product_returns_204_without_body():
    response = client.delete("/products/1")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/products/1").status_code == 404


def test_delete_missing_product_returns_404():
    assert client.delete("/products/99999").status_code == 404


def test_filter_products_by_category_id():
    response = client.get("/products", params={"category_id": 1})
    assert response.status_code == 200
    assert all(item["category_id"] == 1 for item in response.json())


def test_search_products_by_name():
    response = client.get("/products", params={"search": "mouse"})
    assert response.status_code == 200
    assert len(response.json()) == 1
