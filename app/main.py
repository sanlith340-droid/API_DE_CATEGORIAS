from fastapi import FastAPI, HTTPException, Response, status


from app.database import products_db

from app.schemas import Product, ProductCreate, ProductUpdate

app = FastAPI(
    title="Product API",
    description="A simple API for managing products",
    version="1.0.0"
) 

@app.get("/")
def root():
    return {"message": "Hello, World! api Functional!"}


@app.get("/products/", response_model=list[Product])
def get_product(category: str | None = None, available: bool | None = None, search: str | None = None):
    result = products_db
    if category is not None:
        result = [
            product
            for product in result
            if product["category"].lower() == category.lower()
        ]
    if available is not None:
        result = [
            product
            for product in result
            if product["available"] == available

    
        ]

    if search is not None:
        result = [
            product
            for product in result
            if search.lower() in product["name"].lower()
        ]

    return result

@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def get_next_product_id() -> int:
    if not products_db:
        return 1
    return max(product["id"] for product in products_db) + 1

@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED      )
def create_product(product: ProductCreate):

    new_product = { "id": get_next_product_id(), **product.model_dump() } 
    # esta línea crea un nuevo diccionario que combina el ID generado 
    # y los datos del producto proporcionados en la solicitud. El operador ** 
    # se utiliza para desempaquetar el diccionario devuelto por product.model_dump() 
    # y combinarlo con el diccionario que contiene el ID. Esto asegura que el nuevo producto
    #  tenga un ID único y todos los campos necesarios.
    products_db.append(new_product)
    return new_product
    

@app.patch("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductUpdate):
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        product[key] = value
    
    return product



@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int):
    global products_db
    product = next((product for product in products_db if product["id"] == product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    products_db.remove(product)
    return product

@app.get("/health")
def health_check():
    return {"status": "healthy"}