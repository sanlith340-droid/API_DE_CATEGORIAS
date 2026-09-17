# Plan de Pruebas

## 1. Información general

Proyecto: Products API (incluye recurso Categorías)
Versión: 1.0.0
Repositorio base: Modulo_3_SANTIAGO
Tecnologías: Python, FastAPI, Pydantic, pytest, TestClient
Responsable de pruebas: Santiago Buitrago Goyeneche
Fecha de elaboración: Septiembre de 2026

## 2. Objetivo

Verificar que la API de productos y categorías cumpla los requisitos
funcionales y las reglas de negocio establecidas para el CRUD de ambos
recursos, considerando entradas válidas, inválidas y casos límite, y
confirmando la consistencia de los códigos de estado HTTP devueltos.

## 3. Alcance

### Incluido

- CRUD de productos: `POST /products`, `GET /products/`, `GET /products/{id}`,
  `PATCH /products/{id}`, `DELETE /products/{id}`.
- Filtros de listado de productos: `category`, `available`, `search`.
- CRUD de categorías: `POST /categories`, `GET /categories`,
  `GET /categories/{id}`, `PATCH /categories/{id}`, `DELETE /categories/{id}`.
- Filtros de listado de categorías: `active`, `search`.
- Validación de campos obligatorios y rangos (`name`, `price`, `stock`,
  `category`, `description`, `active`).
- Códigos de estado HTTP devueltos por cada operación.
- Estructura JSON de las respuestas.
- Manejo de identificadores de recurso inexistentes (404) e inválidos (422).

### Fuera de alcance

- Autenticación y autorización.
- Pruebas de carga y rendimiento.
- Seguridad especializada (inyección, fuzzing, OWASP).
- Interfaz gráfica (el proyecto no expone una).
- Persistencia real en base de datos (el proyecto usa listas en memoria).
- Validación de que `category` (texto libre en `ProductCreate`) corresponda
  a una categoría existente en `categories_db`: el modelo actual no
  implementa esa relación como llave foránea, por lo que queda fuera de
  este ciclo y se documenta como riesgo aceptado (ver R05 en la sección 4).

## 4. Riesgos

| ID | Riesgo | Probabilidad | Impacto | Prioridad |
|---|---|---|---|---|
| R01 | Aceptar `price` igual o menor que cero al crear/actualizar un producto | Alta | Alto | Crítica |
| R02 | Aceptar `stock` negativo al crear/actualizar un producto | Alta | Alto | Crítica |
| R03 | Inconsistencia entre el método HTTP esperado (`PUT`) y el implementado (`PATCH`) para actualización total de productos | Alta | Alto | Crítica |
| R04 | Endpoint de listado de productos registrado con barra final (`/products/`) y no accesible sin ella (`/products`), rompiendo integraciones que usen la ruta sin barra | Alta | Medio | Alta |
| R05 | `category` es texto libre: se puede crear un producto con una categoría que no existe en `categories_db`, generando datos inconsistentes | Media | Medio | Media |
| R06 | Código de estado inconsistente entre `DELETE /products/{id}` (200 con cuerpo) y `DELETE /categories/{id}` (204 sin cuerpo) | Media | Bajo | Media |
| R07 | Consultar o eliminar un producto/categoría con un ID inexistente y no recibir un 404 claro | Alta | Medio | Alta |
| R08 | Aceptar un nombre de producto o categoría vacío o demasiado corto | Media | Medio | Media |

Justificación de prioridad: R01, R02 y R03 se marcan como críticos porque
afectan directamente reglas de negocio o el contrato del CRUD (verbo HTTP
esperado por cualquier cliente REST estándar). R04 se prueba primero por su
alta probabilidad de romper integraciones simples. R05 y R06 quedan en
prioridad media porque son inconsistencias de diseño, no rechazos de datos
inválidos.

## 5. Estrategia

Se aplicarán pruebas funcionales, positivas, negativas y de frontera sobre
ambos recursos (productos y categorías). Las verificaciones repetibles se
automatizan con `pytest` y `TestClient` de FastAPI, reutilizando y
ampliando la suite existente en `test/test_products.py` y
`test/test_categories.py`.

| Tipo | Propósito | Ejemplo en este proyecto |
|---|---|---|
| Funcional | Verificar que un requisito produzca el comportamiento esperado | `POST /products` crea un producto válido |
| Positiva | Usar datos válidos | `price=49.99`, `stock=10` |
| Negativa | Usar una condición inválida | `price=-10.00` |
| Frontera | Probar valores en el límite permitido/no permitido | `stock=0` frente a `stock=-1` |
| Automatizada | Ejecutar verificaciones repetibles mediante código | `pytest -v` sobre `test/` |

## 6. Ambiente

Sistema operativo: Windows / Linux
Lenguaje: Python 3.12+
Framework: FastAPI 0.141.1
Servidor: Uvicorn 0.52.4
Framework de pruebas: pytest 8.4.2
Cliente HTTP: TestClient (Starlette/httpx)
Almacenamiento de pruebas: listas en memoria (`app/database.py`), sin base
de datos externa

Comando de instalación:

```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Comando de ejecución de la suite:

```
python -m pytest -v
```

Regla de trabajo: al ser datos en memoria reiniciados por los fixtures
`reset_products_db` y `reset_categories_db`, cada prueba parte de un
estado conocido y no requiere una base de datos de producción.

## 7. Datos de prueba

### Productos

| Escenario | Datos relevantes | Resultado esperado |
|---|---|---|
| Producto válido | `name="Auriculares"`, `price=49.99`, `stock=10`, `category="Electronics"` | Aceptado (201) |
| Precio inválido | `price=-10.00` | Rechazado (422) |
| Stock frontera aceptado | `stock=0` | Aceptado |
| Stock inválido | `stock=-1` | Rechazado (422) |
| Nombre demasiado corto | `name="A"` (mínimo 2 caracteres) | Rechazado (422) |
| Nombre faltante | JSON sin `name` | Rechazado (422) |
| ID inexistente | `GET /products/999` | 404 `Product not found` |
| ID inválido | `GET /products/abc` | 422 |

### Categorías

| Escenario | Datos relevantes | Resultado esperado |
|---|---|---|
| Categoría válida | `name="Impresoras"`, `description="Impresoras y consumibles"` | Aceptado (201) |
| Nombre demasiado corto | `name="PC"` (mínimo 3 caracteres) | Rechazado (422) |
| Nombre faltante | JSON sin `name` | Rechazado (422) |
| ID inexistente | `GET /categories/999` | 404 `Category not found` |
| ID inválido | `GET /categories/abc` | 422 |

## 8. Criterios de entrada

- La API inicia correctamente con `uvicorn app.main:app`.
- Los endpoints del alcance (productos y categorías) están implementados.
- `pytest`, `fastapi` y `httpx` están instalados según `requirements.txt`.
- Los datos iniciales de `app/database.py` están disponibles.
- Los requisitos funcionales y reglas de negocio de este documento están
  definidos y acordados.

## 9. Criterios de suspensión

- La API no puede iniciar (error de importación o de arranque de Uvicorn).
- Los módulos `app.database`, `app.schemas` o `app.main` lanzan una
  excepción no controlada al cargar.
- Existe un defecto bloqueante que impide ejecutar los casos críticos
  (por ejemplo, si `POST /products` dejara de responder).

## 10. Criterios de reanudación

- El defecto bloqueante fue corregido y verificado con retest.
- La API vuelve a iniciar sin errores.
- La versión corregida está disponible en el entorno de pruebas.

## 11. Criterios de salida

- 100 % de los casos críticos ejecutados.
- 0 defectos críticos abiertos relacionados con reglas de negocio
  (`price > 0`, `stock >= 0`, nombre obligatorio).
- Al menos 90 % de los casos totales aprobados.
- Las inconsistencias de contrato HTTP (R03, R04, R06) quedan registradas
  como defectos, aunque su corrección pueda planificarse para un ciclo
  posterior si no son bloqueantes para el uso actual de la API.
