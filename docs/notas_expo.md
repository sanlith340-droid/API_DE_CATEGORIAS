# Notas para la exposición — API con FastAPI (Módulo III)

Este documento resume, a partir de la guía de la actividad autónoma (PDF) y de una
revisión real del código del proyecto, lo que debes tener claro para explicar y
defender tu trabajo frente al docente o los compañeros.

---

## 1. De qué trata la actividad (contexto que debes poder explicar)

**API REST de Categorías** para una tienda tecnológica,
sin base de datos real (todo en memoria), aplicando:

- Modelos Pydantic (`CategoryCreate`, `CategoryUpdate`, `Category`)
- CRUD completo con códigos HTTP correctos
- Validaciones (longitud de texto, tipos, valores por defecto)
- Un filtro por query param (`active`)
- Pruebas automatizadas con `pytest` + `TestClient`

**Actualización:** el proyecto original solo tenía la API de **Productos**
(`Product`). Se agregó la API de **Categorías** (`Category`) siguiendo
exactamente el modelo, endpoints y matriz de pruebas del PDF (ver sección 9
de este documento). 

---

## 2. Arquitectura del proyecto (para explicar la estructura)

```
app/
 ├── main.py       -> rutas (endpoints) y lógica de negocio
 ├── schemas.py    -> modelos Pydantic (validación de entrada/salida)
 └── database.py   -> "base de datos" en memoria (lista de diccionarios)
test/
 └── test.products.py -> pruebas con pytest + TestClient
```

Puntos clave que debes poder explicar:

- **`schemas.py`** separa tres modelos: `ProductCreate` (lo que el cliente
  envía al crear), `Product` (lo que la API devuelve, incluye `id`) y
  `ProductUpdate` (todos los campos opcionales, para PATCH).
- **`database.py`** simula la base de datos con una lista de diccionarios en
  memoria. Esto es intencional según el PDF: no se usa base de datos real, el
  foco está en el comportamiento HTTP y las pruebas.
- **`main.py`** define los endpoints usando decoradores de FastAPI
  (`@app.get`, `@app.post`, `@app.patch`, `@app.delete`) y usa `HTTPException`
  para devolver 404 cuando un recurso no existe.

---

## 3. Validaciones con Pydantic (concepto central del módulo)

Explica que Pydantic valida automáticamente los datos de entrada **antes** de
que tu código se ejecute:

- Si un campo obligatorio falta, o no cumple una restricción (`min_length`,
  `max_length`, `gt`, `ge`), FastAPI responde automáticamente con
  **422 Unprocessable Entity** y un JSON con el detalle del error — sin que
  tú escribas ese código a mano.
- El `id` nunca lo define el cliente: lo genera el servidor
  (`get_next_product_id`), tal como exige el PDF.
- `ProductUpdate` usa todos los campos opcionales (`str | None = None`) y en
  el endpoint PATCH se usa `model_dump(exclude_unset=True)` para actualizar
  **solo** los campos que el cliente envió (actualización parcial real, no
  sobrescribir todo el objeto).

---

## 4. Códigos HTTP usados (pregunta típica de evaluación)

| Código | Cuándo se usa en tu API | Dónde |
|---|---|---|
| 200 | Consulta u operación exitosa | GET, PATCH |
| 201 | Recurso creado correctamente | POST |
| 404 | Recurso no encontrado | GET/PATCH/DELETE por id inexistente |
| 422 | Datos inválidos (Pydantic los rechaza) o tipo de dato incorrecto en la URL | POST/PATCH inválidos, `/products/abc` |

---

## 5. Pruebas automatizadas: qué defender

- Usan `TestClient` de `fastapi.testclient`, que simula peticiones HTTP sin
  levantar un servidor real.
- Hay un **fixture `autouse=True`** (`reset_products_db`) que limpia y
  reconstruye la lista `products_db` antes de cada test. Esto es clave: evita
  que una prueba "contamine" a otra (por ejemplo, que un DELETE en un test
  afecte el resultado del siguiente). Es exactamente lo que pide el punto 10
  del PDF.
- Hay casos positivos (crear, listar, consultar, actualizar, eliminar) y
  negativos (id inexistente, id inválido, precio negativo).
- Patrón **Arrange / Act / Assert** usado explícitamente en varias pruebas —
  menciónalo si te preguntan por buenas prácticas de testing.

---

## 6. Hallazgos importantes al ejecutar el proyecto (revísalos antes de entregar)

Se ejecutó el proyecto de forma aislada para verificar su comportamiento real.
Esto es justo lo que un evaluador probablemente hará, así que conviene que lo
sepas de antemano:

### 6.1 `pytest -v` no detecta ninguna prueba tal como está el archivo

El archivo de pruebas se llama **`test.products.py`**. Pytest, por defecto,
solo descubre automáticamente archivos con el patrón `test_*.py` o
`*_test.py`. Con un punto (`test.products.py`) **no lo reconoce**, y al
correr `pytest -v` en la raíz del proyecto el resultado es:

```
collected 0 items
no tests ran in 0.00s
```

**Solución:** renombrar el archivo a `test_products.py`.

### 6.2 Con el nombre corregido, la suite corre pero falla 6 de 13 pruebas

Al renombrar el archivo y ejecutar `pytest -v`, el resultado real fue:
**7 pruebas pasaron, 6 fallaron.** Detalle de las fallas y su causa:

| Prueba | Falla | Causa raíz |
|---|---|---|
| `test_get_products` | 405 en vez de 200 | La ruta está definida como `/products/` (con slash) pero el test llama `/products` (sin slash). Como también existe una ruta POST exacta en `/products` (sin slash), FastAPI no redirige automáticamente y responde "Method Not Allowed". |
| `test_filter_available_products` | 405 en vez de 200 | Misma causa: filtra sobre `/products?available=true`, sin slash. |
| `test_filter_products_by_category` | 405 en vez de 200 | Misma causa, con `/products?category=Laptops`. |
| `test_update_product` | 405 en vez de 200 | El test usa `client.put(...)`, pero en `main.py` **no existe** un endpoint PUT — solo se implementó PATCH. |
| `test_update_non_existing_product` | 405 en vez de 404 | Misma causa: no hay endpoint PUT. |
| `test_delete_product` | 200 en vez de 204 | El endpoint DELETE devuelve `response_model=Product` con código 200 por defecto. El PDF (y el propio test) esperan **204 No Content**, que además no debería devolver cuerpo en la respuesta. |

**Esto es lo más importante que debes revisar antes de exponer o entregar**, porque:
1. Confirma que la condición de aprobación *"la suite de pruebas se ejecuta
   correctamente"* no se cumple todavía tal como está el proyecto.
2. Son errores fáciles de explicar y corregir si te los preguntan en vivo:
   - Unificar la ruta de listado a `/products` (sin slash) en todos lados, o
     usar consistentemente `/products/` en el decorador y en los tests.
   - Agregar un endpoint `PUT /products/{id}` si se quiere actualización
     completa, o corregir los tests para que usen PATCH.
   - Cambiar el DELETE para devolver `204` sin cuerpo, por ejemplo:
     ```python
     @app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
     def delete_product(product_id: int):
         ...
         products_db.remove(product)
         return Response(status_code=204)
     ```

### 6.3 Detalles menores (no rompen la app, pero son buenos puntos a mencionar)

- Existe un archivo `app/__init___.py` (con un guion bajo de más). No afecta
  la ejecución porque Python 3 soporta *namespace packages* sin `__init__.py`,
  pero conviene renombrarlo a `__init__.py` por prolijidad.
- `schemas.py` usa `example=` dentro de `Field(...)`, lo cual Pydantic v2
  marca como **deprecado** (advertencia, no error). La forma recomendada hoy
  es `json_schema_extra={"example": ...}` o el parámetro `examples=[...]`.
- El `requirements.txt` fue generado con `pip freeze`, por lo que incluye
  bastantes dependencias transitivas (más de las estrictamente necesarias).
  Es válido, pero si preguntan por qué hay tantas librerías, esa es la razón.

---

## 7. Preguntas frecuentes que podrían hacerte en la exposición

- **¿Por qué 422 y no 400 para datos inválidos?** Porque es el código que
  FastAPI/Pydantic usa por defecto para errores de validación de esquema; 400
  se reserva típicamente para errores de negocio definidos por ti.
- **¿Por qué usar `TestClient` en vez de probar manualmente en Swagger?**
  Porque permite automatizar, repetir y versionar las pruebas; Swagger sirve
  para verificación manual/exploratoria, no para regresión continua.
- **¿Qué pasa si no reseteas la base de datos entre pruebas?** Los resultados
  dependerían del orden de ejecución (por ejemplo, borrar un producto en una
  prueba haría fallar otra que espera que exista) — por eso el fixture
  `autouse=True` es central para la independencia de las pruebas.
- **¿Cómo generarías el "reto opcional" de búsqueda (`search`)?** Ya está
  implementado parcialmente en `get_product` (filtra por `search` en el
  nombre, sin distinguir mayúsculas/minúsculas con `.lower()`); solo faltaría
  documentarlo y añadir sus pruebas específicas si se exige por separado.

---

## 8. Checklist rápido antes de entregar/exponer (API de Productos)

- [ ] Renombrar `test.products.py` → `test_products.py`
- [ ] Unificar el uso de slash final en las rutas (`/products` vs `/products/`)
- [ ] Decidir: ¿implementar PUT, o dejar solo PATCH y ajustar los tests?
- [ ] Corregir DELETE para responder `204` sin cuerpo
- [ ] Ejecutar `pytest -v` y confirmar que las 13 pruebas pasan
- [ ] Tomar captura de Swagger (`/docs`) con todos los endpoints
- [ ] Tomar captura de la consola con `pytest -v` en verde

Estos puntos son válidos para la API de **Productos**, que se dejó tal como
estaba. La API de **Categorías** (sección 9) sí se entrega ya corregida y con
sus 14 pruebas en verde.

---

## 9. API de Categorías — lo que se agregó siguiendo el PDF

Se implementó exactamente lo que pide la actividad autónoma, dentro del mismo
proyecto (no se tocó la API de Productos):

- **`app/schemas.py`**: se añadieron `CategoryCreate`, `Category` y
  `CategoryUpdate`, con las reglas exactas del PDF (`name` 3-50 caracteres,
  `description` opcional máx. 200 caracteres, `active` booleano con `True`
  por defecto, `id` generado por el servidor).
- **`app/database.py`**: se añadió `categories_db`, una lista en memoria con
  dos categorías iniciales.
- **`app/main.py`**: se añadieron los 5 endpoints obligatorios
  (`GET /categories`, `GET /categories/{id}`, `POST /categories`,
  `PATCH /categories/{id}`, `DELETE /categories/{id}`), el filtro
  `?active=` y el reto opcional `?search=` (búsqueda por nombre, sin
  distinguir mayúsculas/minúsculas).
- **`test/test_categories.py`** (nombre correcto para que `pytest` lo
  descubra automáticamente): 12 pruebas de la matriz CA01–CA12 más 2 pruebas
  del reto opcional.

### 9.1 Decisiones tomadas para no repetir los errores de Productos

Como en la API de Productos se detectaron bugs reales al ejecutar la suite
(sección 6), en Categorías se evitaron a propósito:

- Todas las rutas se registraron **sin slash final** de forma consistente
  (`/categories`, no `/categories/`), así que no hay conflicto entre el GET
  de listado y el POST de creación.
- El `DELETE` usa `status_code=status.HTTP_204_NO_CONTENT` y devuelve
  `Response(status_code=204)` **sin cuerpo**, tal como exige el PDF (a
  diferencia del DELETE de Productos, que devolvía 200 con el objeto).
- Los ejemplos de los esquemas (`Field(..., json_schema_extra={...})`) se
  escribieron con la sintaxis actual de Pydantic v2, evitando la advertencia
  de deprecación que sí aparece en `schemas.py` para Productos.

### 9.2 Resultado real de la ejecución

```
$ pytest test/test_categories.py -v
...
14 passed, 10 warnings in 0.84s
```

Las 12 pruebas obligatorias y las 2 del reto opcional pasan. Las advertencias
que aparecen son deprecaciones de Pydantic que vienen de `schemas.py` en los
modelos de **Productos** (`example=` en `Field`), no de Categorías.

### 9.3 Puntos para defender en la exposición

- **¿Por qué `search` no distingue mayúsculas/minúsculas?** Se comparan
  ambas cadenas en minúscula (`.lower()`) antes del `in`, tal como pide el
  reto opcional del PDF.
- **¿Por qué el DELETE no devuelve el objeto eliminado?** Porque el
  estándar HTTP para `204 No Content` es no incluir cuerpo en la respuesta;
  el cliente ya sabe qué recurso borró (lo pidió por `id`).
- **¿Qué pasa si mandas `id` en el body de un POST?** Se ignora: el modelo
  `CategoryCreate` no tiene el campo `id`, así que Pydantic lo descarta y el
  servidor asigna el siguiente id disponible con `get_next_category_id()`.
- **¿Cómo se prueba que el filtro `active` funciona sin afectar el resto de
  pruebas?** Gracias al fixture `autouse=True`, cada prueba arranca con
  exactamente las mismas dos categorías iniciales (una activa, una inactiva),
  así el resultado del filtro es predecible en cualquier orden de ejecución.

### 9.4 Checklist — API de Categorías

- [x] Modelos `CategoryCreate`, `CategoryUpdate`, `Category` con las reglas del PDF
- [x] 5 endpoints CRUD + filtro `active` + reto opcional `search`
- [x] 404 para categoría inexistente, 422 para datos inválidos
- [x] DELETE responde 204 sin cuerpo
- [x] 14 pruebas automatizadas, todas en verde
- [x] README actualizado con la documentación de la API de Categorías
- [ ] Tomar captura de Swagger (`/docs`) mostrando los endpoints de `/categories`
- [ ] Tomar captura de consola con `pytest test/test_categories.py -v` en verde
