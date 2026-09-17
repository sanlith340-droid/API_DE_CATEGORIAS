# Registro de Defectos

Todos los defectos de este documento fueron reproducidos ejecutando
`python -m pytest -v` sobre el repositorio `Modulo_3_SANTIAGO` tal como
fue entregado, con `fastapi==0.141.1`, `pytest==8.4.2` y
`httpx==0.28.1`.

---

## DEF-001

Título: `GET /products` responde HTTP 405 en lugar de HTTP 200 cuando se
consulta sin barra final.
Severidad: Alta
Prioridad: Alta
Endpoints afectados: `GET /products`, `GET /products?available=true`,
`GET /products?category=Laptops` (cualquier consulta al listado sin la
barra final).
Casos relacionados: CP007, CP008, CP009
Precondición: la API está disponible.

Pasos para reproducir:
1. Iniciar la API o instanciar `TestClient(app)`.
2. Ejecutar `GET /products` (sin barra final).
3. Revisar el código de estado de la respuesta.

Resultado esperado: HTTP 200 y la lista de productos, igual que si se
consultara `/products/`.

Resultado obtenido: HTTP 405 Method Not Allowed. La ruta solo está
registrada como `@app.get("/products/", ...)` (con barra final) en
`app/main.py`; una solicitud a `/products` no se redirige a `/products/`
en este proyecto y termina en un método no permitido.

Evidencia:
```python
>>> client.get('/products').status_code
405
>>> client.get('/products/').status_code
200
```

Estado: Abierto
Nota: todos los tests de `test/test_products.py` que consultan el
listado usan la ruta sin barra final (`/products`), por lo que este
defecto por sí solo explica 3 de los 6 casos fallidos de la suite
original.

---

## DEF-002

Título: La actualización completa de un producto vía `PUT` no está
implementada; la API solo expone `PATCH`.
Severidad: Alta
Prioridad: Alta
Endpoint: `PUT /products/{product_id}`
Casos relacionados: CP013, CP015
Precondición: existe al menos un producto con `id=1`.

Pasos para reproducir:
1. Ejecutar `PUT /products/1` con un JSON de producto completo y válido.
2. Revisar el código de estado de la respuesta.

Resultado esperado: HTTP 200 y el producto actualizado con los valores
enviados (contrato REST estándar: `PUT` reemplaza el recurso completo).

Resultado obtenido: HTTP 405 Method Not Allowed. `app/main.py` únicamente
define `@app.patch("/products/{product_id}", ...)`; no existe un
manejador para el verbo `PUT` sobre ese recurso.

Estado: Abierto
Nota: como consecuencia, `CP015` (actualizar un producto inexistente)
tampoco puede verificar el 404 esperado, porque la solicitud falla antes
por el verbo no soportado.

---

## DEF-003

Título: `DELETE /products/{product_id}` devuelve HTTP 200 con el
producto en el cuerpo, en lugar de HTTP 204 sin cuerpo.
Severidad: Media
Prioridad: Media
Endpoint: `DELETE /products/{product_id}`
Caso relacionado: CP016
Precondición: existe al menos un producto con `id=1`.

Pasos para reproducir:
1. Ejecutar `DELETE /products/1`.
2. Revisar el código de estado y el cuerpo de la respuesta.

Resultado esperado: HTTP 204 No Content, sin cuerpo (igual que el
comportamiento ya implementado en `DELETE /categories/{category_id}`).

Resultado obtenido: HTTP 200 con el JSON del producto eliminado en el
cuerpo de la respuesta.

Evidencia:
```python
>>> r = client.delete('/products/1')
>>> r.status_code, r.json()
(200, {'name': 'Product 1', 'category': 'Laptops', 'price': 10.99, 'stock': 100, 'available': True, 'id': 1})
```

Estado: Abierto
Nota: el producto sí se elimina correctamente de `products_db` (el
efecto funcional es correcto); el defecto es únicamente de contrato
HTTP/consistencia con el endpoint equivalente de categorías.

---

## Severidad vs. prioridad aplicadas

| Defecto | Severidad | Justificación | Prioridad | Justificación |
|---|---|---|---|---|
| DEF-001 | Alta | Rompe el uso normal del listado, el endpoint más usado de la API | Alta | Bloquea integraciones simples de inmediato |
| DEF-002 | Alta | El verbo estándar para "reemplazar recurso" no existe, contrato REST incompleto | Alta | Afecta cualquier cliente que siga la convención `PUT` para actualización completa |
| DEF-003 | Media | El dato se elimina correctamente; solo cambia el código/cuerpo de la respuesta | Media | No bloquea el uso, pero genera inconsistencia frente a `categories` |

## Retest y regresión (una vez corregidos)

Para cada defecto, el retest reejecuta únicamente el caso que lo detectó:

```
pytest -v test/test_products.py -k test_get_products
pytest -v test/test_products.py -k test_update_product
pytest -v test/test_products.py -k test_delete_product
```

Después del retest de cada corrección se debe ejecutar la regresión
completa para confirmar que no se afectaron otros comportamientos:

```
pytest -v
```
