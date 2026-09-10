from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Product Name")
    category: str = Field(..., min_length=2, max_length=100, example="Category Name")
    price: float = Field(..., gt=0, example=19.99)
    stock: int = Field(..., ge=0, example=100)
    available: bool | None = None



class Product(ProductCreate):
    id: int 

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100, example="Updated Product Name")
    category: str | None = Field(None, min_length=2, max_length=100, example="Updated Category Name")
    price: float | None = Field(None, gt=0, example=29.99)
    stock: int | None = Field(None, ge=0, example=50)
    available: bool | None = None