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


def test_list_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_existing_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Periféricos"


def test_get_missing_category_returns_404():
    response = client.get("/categories/99999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Category not found"}


def test_get_invalid_category_id_returns_422():
    assert client.get("/categories/abc").status_code == 422


def test_create_category_valid():
    response = client.post("/categories", json={"name": "Computadores"})
    assert response.status_code == 201
    assert response.json()["name"] == "Computadores"


def test_category_name_shorter_than_three_returns_422():
    assert client.post("/categories", json={"name": "AB"}).status_code == 422


def test_category_name_exactly_three_characters_is_valid():
    assert client.post("/categories", json={"name": "Red"}).status_code == 201


def test_category_name_missing_returns_422():
    assert client.post("/categories", json={}).status_code == 422


def test_duplicate_category_name_is_case_insensitive():
    response = client.post("/categories", json={"name": "audio"})
    assert response.status_code == 409
    assert response.json() == {"detail": "Category name already exists"}


def test_category_name_length_sixty_is_valid():
    response = client.post("/categories", json={"name": "A" * 60})
    assert response.status_code == 201


def test_category_name_length_sixty_one_returns_422():
    assert client.post("/categories", json={"name": "A" * 61}).status_code == 422


def test_update_category_name():
    response = client.patch("/categories/1", json={"name": "Periferia"})
    assert response.status_code == 200
    assert response.json()["name"] == "Periferia"


def test_update_category_duplicate_returns_409():
    assert client.patch("/categories/1", json={"name": "audio"}).status_code == 409


def test_delete_category_returns_204_without_body():
    response = client.delete("/categories/1")
    assert response.status_code == 204
    assert response.content == b""
