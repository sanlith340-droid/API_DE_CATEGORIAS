products_db: list[dict] = [
    {"id": 1, "name": "Product 1", "category": "Laptops", "price": 10.99, "stock": 100, "available": True},
    {"id": 2, "name": "Product 2", "category": "Cameras", "price": 15.99, "stock": 50, "available": True},
    {"id": 3, "name": "Product 3", "category": "Laptops", "price": 20.99, "stock": 0, "available": False},
    {"id": 4, "name": "Product 4", "category": "Cameras", "price": 25.99, "stock": 30, "available": True},
    {"id": 5, "name": "Product 5", "category": "Laptops", "price": 30.99, "stock": 20, "available": True},
]

categories_db: list[dict] = [
    {"id": 1, "name": "Computadores", "description": "Equipos de cómputo", "active": True},
    {"id": 2, "name": "Periféricos", "description": "Accesorios y periféricos", "active": True},
]