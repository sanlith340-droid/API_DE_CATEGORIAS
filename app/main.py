# ═══════════════════════════════════════════════════════════════
# TechStore API v1.0 — API en memoria (sin BD real) que se AUDITA
# contra el contrato del Módulo IV: EP01–EP08, RF01–RF12, RN01–RN08.
#
# Ruta de una petición:
#   1) Pydantic valida el cuerpo/ruta ........ falla → 422
#   2) La función aplica reglas de negocio ... falla → 404 / 409
#   3) FastAPI serializa con response_model .. éxito → 200 / 201 / 204
# Marca "EXTRA" = existe en el código pero NO está en el contrato.
# ═══════════════════════════════════════════════════════════════
from fastapi import FastAPI, HTTPException, Response, status

from app.database import categories_db, products_db
from app.schemas import Category, CategoryCreate, CategoryUpdate, Product, ProductCreate, ProductUpdate

app = FastAPI(
    title="TechStore Products & Categories API",
    description="API en memoria auditada contra el contrato del Módulo IV.",
    version="1.0.0",
)


# ── Funciones auxiliares ────────────────────────────────────────

# El id lo genera el servidor (máximo actual + 1); el cliente nunca lo envía.
def next_id(items: list[dict]) -> int:
    return max((item["id"] for item in items), default=0) + 1


# Devuelve el registro o None; el endpoint decide si responde 404.
def find_category(category_id: int) -> dict | None:
    return next((category for category in categories_db if category["id"] == category_id), None)


def find_product(product_id: int) -> dict | None:
    return next((product for product in products_db if product["id"] == product_id), None)


# RN06: la categoría del producto debe existir → 404 (no 422).
def ensure_category_exists(category_id: int) -> None:
    if find_category(category_id) is None:
        raise HTTPException(status_code=404, detail="Category not found")


# RN02: nombre único SIN distinguir mayúsculas → 409.
# casefold() iguala "Audio" y "audio". exclude_id deja que PATCH conserve su propio nombre.
def ensure_unique_category_name(name: str, exclude_id: int | None = None) -> None:
    normalized = name.casefold()
    duplicate = next(
        (category for category in categories_db
         if category["id"] != exclude_id and category["name"].casefold() == normalized),
        None,
    )
    if duplicate is not None:
        raise HTTPException(status_code=409, detail="Category name already exists")


# ── Utilidades (EXTRA) ──────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Prueba del server santiago buitrago"}


# EXTRA: sirve para el criterio de entrada "la API inicia correctamente".
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ── CATEGORÍAS ──────────────────────────────────────────────────

# EP02 · RF02 → 200. response_model=Category solo expone id y name.
@app.get("/categories", response_model=list[Category])
def list_categories():
    return categories_db


# EP03 · RF03 → 200 si existe · RF04 → 404 si no existe.
@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# EP01 · RF01 → 201. RN01 (3–60 caracteres) lo valida Pydantic → 422.
# RN02 (duplicado) se valida aquí → 409.
@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    ensure_unique_category_name(category.name)
    new_category = {"id": next_id(categories_db), **category.model_dump()}
    categories_db.append(new_category)
    return new_category


# EXTRA (fuera del contrato): actualización parcial.
# exclude_unset=True → solo cambia lo que el cliente envió.
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


# EXTRA (fuera del contrato). RIESGO PENDIENTE: no revisa si hay productos
# asociados; al borrar una categoría los productos quedan "huérfanos".
@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    category = find_category(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    categories_db.remove(category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ── PRODUCTOS ───────────────────────────────────────────────────

# EP05 · RF06 → 200. Ruta SIN "/" final (corrige DEF-M4-001: daba 405).
# Los filtros category_id y search son EXTRA (no están en el contrato).
@app.get("/products", response_model=list[Product])
def list_products(category_id: int | None = None, search: str | None = None):
    result = products_db
    if category_id is not None:
        result = [product for product in result if product["category_id"] == category_id]
    if search is not None:
        result = [product for product in result if search.casefold() in product["name"].casefold()]
    return result


# EP06 · RF07 → 200 si existe · RF08 → 404 si no existe.
@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# EP04 · RF05 → 201. RN03/RN04/RN05 los valida Pydantic → 422.
# RN06 (categoría existente) se valida aquí → 404.
@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    ensure_category_exists(product.category_id)
    new_product = {"id": next_id(products_db), **product.model_dump()}
    products_db.append(new_product)
    return new_product


# EP07 · RF09 → 200 · RF10 → 404 · RN08.
# Reutiliza ProductCreate → las MISMAS validaciones que al crear (RN08).
# Orden de errores: 422 (cuerpo) → 404 (producto) → 404 (categoría).
# Ojo: un PUT a un id inexistente con cuerpo inválido responde 422, no 404.
@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductCreate):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    ensure_category_exists(product_update.category_id)
    product.update(product_update.model_dump())
    return product


# EXTRA (fuera del contrato): actualización parcial con PATCH.
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


# EP08 · RF11 → 204 SIN cuerpo (corrige DEF-M4-003: devolvía 200 con objeto)
# · RF12 → 404 si no existe.
@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    product = find_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db.remove(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
