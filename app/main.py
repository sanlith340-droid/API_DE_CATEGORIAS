from fastapi import FastAPI, HTTPException, Response, status

from app.database import categories_db, products_db
from app.schemas import Category, CategoryCreate, CategoryUpdate, Product, ProductCreate, ProductUpdate

app = FastAPI(
    title="TechStore Products & Categories API",
    description="API en memoria auditada contra el contrato del Módulo IV.",
    version="1.0.0",
)


def next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


def find_category(category_id: int) -> dict | None:
    return next((category for category in categories_db if category["id"] == category_id), None)


def find_product(product_id: int) -> dict | None:
    return next((product for product in products_db if product["id"] == product_id), None)


def ensure_category_exists(category_id: int) -> None:
    if find_category(category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")


def ensure_unique_category_name(name: str, exclude_id: int | None = None) -> None:
    normalized = name.casefold()
    duplicate = next(
        (category for category in categories_db
         if category["id"] != exclude_id and category["name"].casefold() == normalized),
        None,
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="Category name already exists")


@app.get("/")
def root():
    return {"message": "Prueba del server santiago buitrago"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/categories", response_model=list[Category])
def list_categories():
    return categories_db


@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    ensure_unique_category_name(category.name)
    new_category = {"id": next_id(categories_db), **category.model_dump()}
    categories_db.append(new_category)
    return new_category


@app.patch("/categories/{category_id}", response_model=Category)
def patch_category(category_id: int, category_update: CategoryUpdate):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    data = category_update.model_dump(exclude_unset=True)
    if "name" in data:
        ensure_unique_category_name(data["name"], exclude_id=category_id)
    category.update(data)
    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    categories_db.remove(category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/products", response_model=list[Product])
def list_products(category_id: int | None = None, search: str | None = None):
    result = products_db
    if category_id is not None:
        result = [product for product in result if product["category_id"] == category_id]
    if search is not None:
        result = [product for product in result if search.casefold() in product["name"].casefold()]
    return result


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    ensure_category_exists(product.category_id)
    new_product = {"id": next_id(products_db), **product.model_dump()}
    products_db.append(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductCreate):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    ensure_category_exists(product_update.category_id)
    product.update(product_update.model_dump())
    return product


@app.patch("/products/{product_id}", response_model=Product)
def patch_product(product_id: int, product_update: ProductUpdate):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    data = product_update.model_dump(exclude_unset=True)
    if "category_id" in data:
        ensure_category_exists(data["category_id"])
    product.update(data)
    return product


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db.remove(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
