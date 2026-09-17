# Casos de Prueba

Convención de identificadores: `CP0xx` para productos, `CAxx` para
categorías (los CA ya existen como comentarios en
`test/test_categories.py`; aquí se documentan formalmente).

Cada caso indica si ya está automatizado en `test/` y, si aplica, qué
defecto detectó (ver `registro-defectos.md`).

---

## Productos

### CP001 — Crear producto correctamente

Requisito: RF01
Prioridad: Alta
Precondición: la API está disponible.
Datos:
```json
{"name": "New Product", "category": "Electronics", "price": 49.99, "stock": 10, "available": true}
```
Pasos:
1. Ejecutar `POST /products`.
2. Enviar el JSON anterior.
3. Revisar la respuesta.

Resultado esperado: HTTP 201 y el producto creado con los mismos datos
enviados más un `id` generado.
Estado: Automatizado (`test_create_product`) — PASSED.

### CP002 — Rechazar precio negativo

Requisito: RN02
Prioridad: Crítica
Datos: igual a CP001 con `"price": -10.00`.
Resultado esperado: HTTP 422, el producto no debe crearse.
Estado: Automatizado (`test_create_product_negative_price`) — PASSED.

### CP003 — Rechazar stock negativo al crear producto

Requisito: RN03
Prioridad: Crítica
Datos: igual a CP001 con `"stock": -1`.
Resultado esperado: HTTP 422, el producto no debe crearse.
Estado: Pendiente de automatizar (brecha detectada en la matriz de
trazabilidad).
Test propuesto:
```python
def test_cp003_create_product_negative_stock(client):
    product = {"name": "Mouse", "category": "Electronics", "price": 10.0, "stock": -1, "available": True}
    response = client.post("/products", json=product)
    assert response.status_code == 422
```

### CP004 — Aceptar stock igual a cero (frontera)

Requisito: RN03
Prioridad: Media
Datos: igual a CP001 con `"stock": 0`.
Resultado esperado: HTTP 201, el producto se crea con `stock=0`.
Estado: Pendiente de automatizar.

### CP005 — Rechazar producto sin nombre

Requisito: RN01
Prioridad: Alta
Datos: JSON de CP001 sin la clave `name`.
Resultado esperado: HTTP 422.
Estado: Pendiente de automatizar.

### CP006 — Rechazar nombre demasiado corto (1 carácter)

Requisito: RN01
Prioridad: Media
Datos: igual a CP001 con `"name": "A"`.
Resultado esperado: HTTP 422 (`name` requiere mínimo 2 caracteres).
Estado: Pendiente de automatizar.

### CP007 — Consultar listado de productos

Requisito: RF02
Prioridad: Alta
Pasos: `GET /products`.
Resultado esperado: HTTP 200 y una lista JSON de productos.
Estado: Automatizado (`test_get_products`) — **FAILED** (HTTP 405 en
lugar de 200). Ver DEF-001.

### CP008 — Filtrar productos por disponibilidad

Requisito: RF02
Prioridad: Media
Pasos: `GET /products?available=true`.
Resultado esperado: HTTP 200 y solo productos con `available=true`.
Estado: Automatizado (`test_filter_available_products`) — **FAILED**
(HTTP 405). Ver DEF-001.

### CP009 — Filtrar productos por categoría

Requisito: RF02
Prioridad: Media
Pasos: `GET /products?category=Laptops`.
Resultado esperado: HTTP 200 y solo productos de la categoría `Laptops`.
Estado: Automatizado (`test_filter_products_by_category`) — **FAILED**
(HTTP 405). Ver DEF-001.

### CP010 — Consultar producto existente por ID

Requisito: RF03
Prioridad: Alta
Pasos: `GET /products/1`.
Resultado esperado: HTTP 200, `id == 1` y el campo `name` presente.
Estado: Automatizado (`test_get_existing_product`) — PASSED.

### CP011 — Consultar producto inexistente por ID

Requisito: RF03 / RN04
Prioridad: Alta
Pasos: `GET /products/999`.
Resultado esperado: HTTP 404, `{"detail": "Product not found"}`.
Estado: Automatizado (`test_get_non_existing_product`) — PASSED.

### CP012 — Consultar producto con ID no numérico

Requisito: RF03
Prioridad: Media
Pasos: `GET /products/abc`.
Resultado esperado: HTTP 422.
Estado: Automatizado (`test_invalid_product_id`) — PASSED.

### CP013 — Actualizar producto completo vía PUT

Requisito: RF04
Prioridad: Alta
Datos:
```json
{"name": "Updated Product", "category": "Updated Category", "price": 59.99, "stock": 20, "available": false}
```
Pasos: `PUT /products/1` con el JSON anterior.
Resultado esperado: HTTP 200 y el producto actualizado con esos valores.
Estado: Automatizado (`test_update_product`) — **FAILED** (HTTP 405: el
verbo `PUT` no está implementado). Ver DEF-002.

### CP014 — Actualizar parcialmente el precio vía PATCH

Requisito: RF04
Prioridad: Alta
Datos: `{"price": 79.99}`.
Pasos: `PATCH /products/1`.
Resultado esperado: HTTP 200 y `price == 79.99`, el resto de campos sin
cambios.
Estado: Automatizado (`test_update_price_patch`) — PASSED.

### CP015 — Actualizar producto inexistente vía PUT

Requisito: RF04
Prioridad: Alta
Pasos: `PUT /products/999` con un JSON de producto válido.
Resultado esperado: HTTP 404, `{"detail": "Product not found"}`.
Estado: Automatizado (`test_update_non_existing_product`) — **FAILED**
(HTTP 405 antes de poder validar el 404). Ver DEF-002.

### CP016 — Eliminar producto existente

Requisito: RF05
Prioridad: Alta
Pasos:
1. `DELETE /products/1`.
2. `GET /products/1`.

Resultado esperado: la respuesta del `DELETE` es HTTP 204 sin cuerpo, y
el `GET` posterior devuelve HTTP 404.
Estado: Automatizado (`test_delete_product`) — **FAILED** (el `DELETE`
devuelve HTTP 200 con el producto en el cuerpo, en vez de 204). Ver
DEF-003. El producto sí queda eliminado (la segunda parte del caso pasa).

### CP017 — Eliminar producto inexistente

Requisito: RF05 / RN05
Prioridad: Media
Pasos: `DELETE /products/999`.
Resultado esperado: HTTP 404, `{"detail": "Product not found"}`.
Estado: Pendiente de automatizar (brecha detectada en la matriz de
trazabilidad).

### CP018 — Verificación de salud del servicio

Requisito: infraestructura (fuera del alcance funcional, pero relevante
como precondición operativa)
Prioridad: Baja
Pasos: `GET /health`.
Resultado esperado: HTTP 200, `{"status": "healthy"}`.
Estado: Automatizado (`test_health`) — PASSED.

---

## Categorías

Los siguientes casos ya están completamente automatizados en
`test/test_categories.py` (identificados allí con los mismos códigos en
comentarios). Se resumen aquí para mantener la trazabilidad del paquete
de documentación.

| ID | Título | Requisito | Resultado esperado | Estado |
|---|---|---|---|---|
| CA01 | Listar categorías | RF07 | HTTP 200, lista con 2 elementos (dataset de prueba) | PASSED |
| CA02 | Consultar categoría existente | RF08 | HTTP 200, `id==1`, `name=="Computadores"` | PASSED |
| CA03 | Consultar categoría inexistente | RF08 / RN07 | HTTP 404, `Category not found` | PASSED |
| CA04 | Consultar con ID no numérico | RF08 | HTTP 422 | PASSED |
| CA05 | Crear categoría válida | RF06 | HTTP 201, categoría creada con `id` | PASSED |
| CA06 | Rechazar nombre demasiado corto (<3 caracteres) | RN06 | HTTP 422 | PASSED |
| CA07 | Rechazar categoría sin nombre | RN06 | HTTP 422 | PASSED |
| CA08 | Actualizar categoría existente (PATCH parcial) | RF09 | HTTP 200, solo el campo enviado cambia | PASSED |
| CA09 | Actualizar categoría inexistente | RF09 / RN08 | HTTP 404 | PASSED |
| CA10 | Eliminar categoría existente | RF10 | HTTP 204 sin cuerpo; `GET` posterior devuelve 404 | PASSED |
| CA11 | Eliminar categoría inexistente | RF10 / RN08 | HTTP 404 | PASSED |
| CA12 | Filtrar categorías activas | RF07 | HTTP 200, solo categorías con `active=true` | PASSED |
| CA13 | Buscar por nombre con resultado | RF07 | HTTP 200, coincidencia case-insensitive | PASSED |
| CA14 | Buscar por nombre sin resultado | RF07 | HTTP 200, lista vacía | PASSED |

Nota de diseño: el módulo de categorías implementa correctamente el
código 204 sin cuerpo en su `DELETE` (`status.HTTP_204_NO_CONTENT` +
`Response(status_code=...)`), lo que se usó como referencia para
detectar la inconsistencia del mismo verbo en productos (DEF-003).
