from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.database import products_db
client = TestClient(app)

INITIAL_PRODUCTS = [
    {"id": 1, "name": "Product 1", "category": "Laptops", "price": 10.99, "stock": 100, "available": True},
    {"id": 2, "name": "Product 2", "category": "Cameras", "price": 15.99, "stock": 50, "available": True},
    {"id": 3, "name": "Product 3", "category": "Laptops", "price": 20.99, "stock": 0, "available": False},
    {"id": 4, "name": "Product 4", "category": "Cameras", "price": 25.99, "stock": 30, "available": True},
    {"id": 5, "name": "Product 5", "category": "Laptops", "price": 30.99, "stock": 20, "available": True},
]

@pytest.fixture(autouse=True)
def reset_products_db():
    # Before each test, reset the products_db to its initial state
    products_db.clear()
    products_db.extend(INITIAL_PRODUCTS)

def test_health():

    #Arrange
    endpoint = "/health"

    #Act
    response = client.get(endpoint)

    #Assert
    assert response.status_code == 200

    assert response.json() == {"status": "healthy"}

def test_get_products():
    # Arrange
    endpoint = "/products"

    # Act
    response = client.get(endpoint)

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_existing_product():

    response = client.get("/products/1")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == 1 # Verify the product ID
    assert "name" in data # Verify the product name is present

def test_get_non_existing_product():
    response = client.get("/products/999")  # Assuming 999 is a non-existing product ID

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_invalid_product_id():
    response = client.get("/products/abc")  # Invalid product ID (not an integer)

    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

def test_filter_available_products():
    response = client.get("/products?available=true")

    assert response.status_code == 200
    data = response.json()
    assert all(product["available"] is True for product in data)
 
def test_filter_products_by_category():
    response = client.get("/products?category=Laptops")

    assert response.status_code == 200
    data = response.json()
    assert all(product["category"] == "Laptops" for product in data)

def test_create_product():
    new_product = {
        "name": "New Product",
        "category": "Electronics",
        "price": 49.99,
        "stock": 10,
        "available": True
    }

    response = client.post("/products", json=new_product)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_product["name"]
    assert data["category"] == new_product["category"]
    assert data["price"] == new_product["price"]
    assert data["stock"] == new_product["stock"]
    assert data["available"] == new_product["available"]

def test_create_product_negative_price():
    new_product = {
        "name": "Invalid Product",
        "category": "Electronics",
        "price": -10.00,  # Invalid negative price
        "stock": 5,
        "available": True
    }

    response = client.post("/products", json=new_product)

    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

def test_update_product():
    updated_product = {
        "name": "Updated Product",
        "category": "Updated Category",
        "price": 59.99,
        "stock": 20,
        "available": False
    }

    response = client.put("/products/1", json=updated_product)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]
    assert data["category"] == updated_product["category"]
    assert data["price"] == updated_product["price"]
    assert data["stock"] == updated_product["stock"]
    assert data["available"] == updated_product["available"]

def test_update_price_patch():
    updated_price = {
        "price": 79.99
    }

    response = client.patch("/products/1", json=updated_price)

    assert response.status_code == 200
    data = response.json()
    assert data["price"] == updated_price["price"]

def test_update_non_existing_product():
    updated_product = {
        "name": "Non-existing Product",
        "category": "Category",
        "price": 99.99,
        "stock": 10,
        "available": True
    }

    response = client.put("/products/999", json=updated_product)  # Assuming 999 is a non-existing product ID

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

def test_delete_product():
    response = client.delete("/products/1")

    assert response.status_code == 204
    data = response.json()
    assert data["id"] == 1

    # Verify that the product is actually deleted
    get_response = client.get("/products/1")
    assert get_response.status_code == 404