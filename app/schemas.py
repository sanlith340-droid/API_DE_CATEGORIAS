from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60, json_schema_extra={"example": "Periféricos"})


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=60, json_schema_extra={"example": "Audio"})


class Category(CategoryCreate):
    id: int


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=80, json_schema_extra={"example": "Teclado mecánico"})
    price: float = Field(..., gt=0, json_schema_extra={"example": 250000})
    stock: int = Field(..., ge=0, json_schema_extra={"example": 10})
    category_id: int = Field(..., json_schema_extra={"example": 1})


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=80)
    price: float | None = Field(None, gt=0)
    stock: int | None = Field(None, ge=0)
    category_id: int | None = None


class Product(ProductCreate):
    id: int
