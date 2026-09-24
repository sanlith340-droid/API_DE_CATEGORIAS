# Plan de pruebas — TechStore API

## 1. Identificación del proyecto y versión auditada

| Campo | Valor |
|---|---|
| Proyecto | TechStore Products & Categories API |
| Versión auditada | 1.0.0 |
| Responsable de la auditoría | Santiago Buitrago Goyeneche |
| Tecnologías | Python, FastAPI, Pydantic, pytest, HTTPX/TestClient |
| Fecha | Septiembre de 2026 |
| Documento base del contrato | PDF del Mini Proyecto Evaluable del Módulo IV |

## 2. Objetivo de la auditoría

Verificar que la API cumpla con el contrato funcional y de negocio definido en el PDF del Mini Proyecto Evaluable del Módulo IV (EP01–EP08, RF01–RF12, RN01–RN08), confirmando que las operaciones de creación, listado, consulta, actualización y eliminación de categorías y productos respondan con los códigos HTTP correctos (200/201/204/404/409/422) y que las reglas de validación y de negocio se apliquen de forma consistente.

## 3. Alcance y fuera de alcance

**Dentro de alcance:**
- CRUD completo de `categories` y `products`.
- Validaciones de esquema (Pydantic): longitud de nombres, tipos de dato, precio y stock.
- Reglas de negocio: unicidad de nombre de categoría (case-insensitive), existencia de `category_id` al crear/actualizar productos.
- Códigos de respuesta HTTP: 200, 201, 204, 404, 409, 422.
- Casos frontera de longitud, precio y stock.
- Ejecución de la suite automatizada (`pytest`) como evidencia de regresión.

**Fuera de alcance:**
- Autenticación y autorización.
- Pruebas de rendimiento/carga.
- Seguridad especializada (pentesting, OWASP, etc.).
- Interfaz de usuario (solo se usa Swagger como apoyo exploratorio).
- Persistencia real en base de datos (el proyecto usa listas en memoria).

## 4. Inventario de endpoints incluidos

| # | Método | Endpoint | Resultado esperado | Estado frente al contrato |
|---|---|---|---|---|
| 1 | GET | `/categories` | 200 | Contrato (RF02) |
| 2 | GET | `/categories/{id}` | 200 / 404 | Contrato (RF03/RF04) |
| 3 | POST | `/categories` | 201 / 409 / 422 | Contrato (RF01/RN01/RN02) |
| 4 | PATCH | `/categories/{id}` | 200 / 404 / 422 | Extra (no exigido por el contrato base) |
| 5 | DELETE | `/categories/{id}` | 204 / 404 | Contrato |
| 6 | GET | `/products` | 200 | Contrato (RF06) |
| 7 | GET | `/products/{id}` | 200 / 404 | Contrato (RF07/RF08) |
| 8 | POST | `/products` | 201 / 404 / 422 | Contrato (RF05/RN03–RN06) |
| 9 | PUT | `/products/{id}` | 200 / 404 / 422 | Contrato (RF09/RF10/RN08) |
| 10 | PATCH | `/products/{id}` | 200 / 404 / 422 | Extra (actualización parcial) |
| 11 | DELETE | `/products/{id}` | 204 / 404 | Contrato (RF11/RF12) |
| 12 | GET | `/` | 200 | Extra (raíz informativa, fuera de contrato) |
| 13 | GET | `/health` | 200 | Extra (health check, apoya criterios de entrada) |

Total: 13 endpoints implementados; 9 pertenecen directamente al contrato auditado y 4 son extensiones del código (`PATCH` en ambos recursos, `/` y `/health`) que no forman parte de los requisitos pero se ejecutan para no dejar comportamiento sin observar.

## 5. Riesgos y priorización

| ID | Riesgo | Probabilidad | Impacto | Prioridad |
|---|---|---:|---:|---:|
| R01 | Producto creado con categoría inexistente | Media | Alto | Alta |
| R02 | Categorías duplicadas por diferencia de mayúsculas/minúsculas | Alta | Alto | Alta |
| R03 | Precio cero o negativo aceptado | Alta | Alto | Alta |
| R04 | Stock negativo aceptado | Media | Alto | Alta |
| R05 | Verbo HTTP o código de respuesta incorrecto (p. ej. 405 en vez de 200, 200 en vez de 204) | Media | Alto | Alta |
| R06 | Límites de longitud de nombre incorrectos o inconsistentes | Media | Media | Media |
| R07 | Inconsistencia de slash final en rutas (`/products` vs `/products/`) | Baja | Medio | Media |

## 6. Estrategia de pruebas

Se combinan cuatro tipos de prueba sobre cada endpoint del inventario (sección 4):

- **Positivas:** creación, listado, consulta, actualización y eliminación con datos válidos (ej. CP-CAT-01, CP-PROD-01, CP-PROD-05).
- **Negativas:** IDs inexistentes, datos inválidos, categoría inexistente, duplicados (ej. CP-CAT-04, CP-CAT-08, CP-PROD-16).
- **De frontera:** límites de longitud de nombre (3 y 60/80 caracteres), precio mínimo (0.01) y precio/stock justo por debajo del límite permitido (ej. CP-CAT-05/06/07, CP-PROD-11/12/13/14/15).
- **Automatizadas:** toda la matriz de casos (`docs/casos-prueba.md`) está implementada en `test/test_categories.py` y `test/test_products.py`, ejecutable con `python -m pytest -v`, con fixtures `autouse=True` que reinician `categories_db` y `products_db` antes de cada prueba para evitar contaminación entre casos.

## 7. Ambiente y herramientas

- **Lenguaje/runtime:** Python 3.12+.
- **Framework:** FastAPI.
- **Validación:** Pydantic v2.
- **Pruebas:** pytest, `fastapi.testclient.TestClient` / HTTPX.
- **Servidor de desarrollo:** uvicorn.
- **Documentación interactiva:** Swagger UI en `http://127.0.0.1:8000/docs`.
- **Sistema operativo:** Linux o Windows (validado en ambos vía scripts de activación de entorno virtual).
- **Persistencia:** listas en memoria (`app/database.py`), sin base de datos real.

## 8. Datos de prueba

| Tipo | Dato | Uso |
|---|---|---|
| Categorías base | `Periféricos`, `Audio` | Precondición de casos positivos y de duplicado |
| Productos base | `Mouse inalámbrico` (precio 120000, stock 5), `Monitor` (precio 850000, stock 0) | Precondición de consulta, actualización y eliminación |
| ID inexistente | `99999` | Casos negativos de 404 (categorías y productos) |
| Nombres frontera | 2 caracteres (`AB`), 3 caracteres (`Red`, `RAM`), 60 caracteres (categoría), 80 caracteres (producto) | Casos frontera de RN01/RN03 |
| Precios frontera | `0`, `-1000`, `0.01` | Casos frontera y negativos de RN04 |
| Stock frontera | `-1`, `0` | Casos frontera y negativos de RN05/RN07 |
| Nombre duplicado | `audio` vs `Audio` existente | Caso negativo de unicidad case-insensitive (RN02) |

## 9. Criterios de entrada

- Dependencias del `requirements.txt` instaladas en el entorno virtual.
- Los módulos `app.main`, `app.schemas` y `app.database` son importables sin errores.
- El servidor inicia correctamente (`uvicorn` levanta la app) y `GET /health` responde 200.
- El contrato (PDF del Módulo IV) está disponible y no ha cambiado desde el último acuerdo con el equipo.

## 10. Criterios de suspensión y reanudación

**Suspensión:** la ejecución se detiene si la aplicación no inicia, si un caso crítico (marcado como prioridad Alta en la matriz de trazabilidad) no puede ejecutarse por un bloqueo de entorno, o si se detecta un defecto crítico que impide continuar con los casos dependientes.

**Reanudación:** se retoma la ejecución una vez corregido el bloqueo o el defecto crítico, realizando primero un retest puntual del caso afectado y luego una regresión de los casos relacionados según la matriz de trazabilidad (`docs/matriz-trazabilidad.md`).

## 11. Criterios de salida

- 100% de los casos críticos (prioridad Alta) ejecutados.
- 100% de las pruebas automatizadas (`python -m pytest -v`) aprobadas.
- Cero defectos críticos o altos abiertos en `docs/registro-defectos.md`.
- Retest y regresión documentados en `docs/informe-ejecucion.md`.
- Evidencia disponible: salida de consola de `pytest -v`, `docs/casos-prueba.md`, `docs/matriz-trazabilidad.md` y `docs/registro-defectos.md`.

**Responsable de ejecución:** Santiago Buitrago Goyeneche.
