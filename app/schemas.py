# ═══════════════════════════════════════════════════════════════
# Modelos Pydantic = primera línea de defensa. Si el dato no cumple,
# FastAPI responde 422 SIN que el endpoint llegue a ejecutarse.
# Field(...) = obligatorio · min/max_length = largo · gt = ">" · ge = ">="
# ═══════════════════════════════════════════════════════════════
from pydantic import BaseModel, Field


# ── Categorías ──────────────────────────────────────────────────

# RN01: nombre obligatorio, entre 3 y 60 caracteres (frontera: 2 ✗, 3 ✓, 60 ✓, 61 ✗).
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, json_schema_extra={"example": "Periféricos"})


# EXTRA (PATCH): campo opcional; si se envía, aplica las mismas restricciones.
class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=60, json_schema_extra={"example": "Audio"})


# Modelo de SALIDA: hereda name y agrega id (lo asigna el servidor).
class Category(CategoryCreate):
    id: int


# ── Productos ───────────────────────────────────────────────────

# RN03: name 3–80 · RN04: price > 0 (gt: el 0 se rechaza)
# RN05/RN07: stock >= 0 (ge: el 0 SÍ se acepta).
# RN06 (category_id existente) NO se valida aquí: es regla de negocio → main.py (404).
# Este mismo modelo se reutiliza en PUT → cumple RN08.
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=80, json_schema_extra={"example": "Teclado mecánico"})
    price: float = Field(..., gt=0, json_schema_extra={"example": 250000})
    stock: int = Field(..., ge=0, json_schema_extra={"example": 10})
    category_id: int = Field(..., json_schema_extra={"example": 1})


# EXTRA (PATCH): todos los campos opcionales, mismas restricciones si se envían.
class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=80)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    category_id: int | None = None


# Modelo de SALIDA: campos de creación + id generado por el servidor.
class Product(ProductCreate):
    id: int
