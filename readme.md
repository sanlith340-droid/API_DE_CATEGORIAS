# TechStore Products & Categories API

API REST desarrollada con FastAPI para el Mini Proyecto Evaluable del Módulo IV — Auditoría completa de pruebas.

## Instalación

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecución

```bash
python -m uvicorn app.main:app --reload
```

Documentación interactiva: <http://127.0.0.1:8000/docs>

## Endpoints principales

| Método | Endpoint | Resultado |
|---|---|---:|
| POST | `/categories` | 201 |
| GET | `/categories` | 200 |
| GET | `/categories/{id}` | 200 / 404 |
| DELETE | `/categories/{id}` | 204 / 404 |
| POST | `/products` | 201 / 404 / 422 |
| GET | `/products` | 200 |
| GET | `/products/{id}` | 200 / 404 |
| PUT | `/products/{id}` | 200 / 404 / 422 |
| DELETE | `/products/{id}` | 204 / 404 |

`PATCH` está disponible como extensión para actualizaciones parciales.

## Contrato de datos

Una categoría contiene `name`, obligatorio entre 3 y 60 caracteres. Los nombres duplicados se rechazan sin distinguir mayúsculas/minúsculas con HTTP 409.

Un producto contiene `name` entre 3 y 80 caracteres, `price > 0`, `stock >= 0` y `category_id` asociado a una categoría existente. Los errores de validación responden 422 y una categoría inexistente responde 404.

## Pruebas

```bash
python -m pytest -v
```

Última ejecución verificada: **35 passed, 0 failed**.

### Comandos por tipo de prueba

Cada bloque ejecuta 5 casos representativos de `test/test_categories.py` y `test/test_products.py` (ver el detalle de cada caso en `docs/casos-prueba.md`).

**5 pruebas positivas** (crean/consultan/actualizan/eliminan con datos válidos):

```bash
python -m pytest test/test_categories.py::test_create_category_valid -v
python -m pytest test/test_categories.py::test_list_categories -v
python -m pytest test/test_products.py::test_create_product_valid -v
python -m pytest test/test_products.py::test_put_product_valid -v
python -m pytest test/test_products.py::test_delete_product_returns_204_without_body -v
```

Combinado en un solo comando:

```bash
python -m pytest -v -k "test_create_category_valid or test_list_categories or test_create_product_valid or test_put_product_valid or test_delete_product_returns_204_without_body"
```

**5 pruebas negativas** (IDs inexistentes, duplicados, datos inválidos):

```bash
python -m pytest test/test_categories.py::test_get_missing_category_returns_404 -v
python -m pytest test/test_categories.py::test_duplicate_category_name_is_case_insensitive -v
python -m pytest test/test_products.py::test_create_product_negative_price_returns_422 -v
python -m pytest test/test_products.py::test_create_product_missing_category_returns_404 -v
python -m pytest test/test_products.py::test_delete_missing_product_returns_404 -v
```

Combinado en un solo comando:

```bash
python -m pytest -v -k "test_get_missing_category_returns_404 or test_duplicate_category_name_is_case_insensitive or test_create_product_negative_price_returns_422 or test_create_product_missing_category_returns_404 or test_delete_missing_product_returns_404"
```

**5 pruebas frontera** (límites de longitud, precio mínimo y stock cero):

```bash
python -m pytest test/test_categories.py::test_category_name_shorter_than_three_returns_422 -v
python -m pytest test/test_categories.py::test_category_name_exactly_three_characters_is_valid -v
python -m pytest test/test_categories.py::test_category_name_length_sixty_is_valid -v
python -m pytest test/test_products.py::test_create_product_minimum_positive_price_is_valid -v
python -m pytest test/test_products.py::test_create_product_stock_zero_is_valid -v
```

Combinado en un solo comando:

```bash
python -m pytest -v -k "test_category_name_shorter_than_three_returns_422 or test_category_name_exactly_three_characters_is_valid or test_category_name_length_sixty_is_valid or test_create_product_minimum_positive_price_is_valid or test_create_product_stock_zero_is_valid"
```

## Auditoría

La carpeta `docs/` contiene:

- `plan-pruebas.md`
- `matriz-trazabilidad.md`
- `casos-prueba.md`
- `registro-defectos.md`
- `informe-ejecucion.md`

La auditoría cubre RF01–RF12, RN01–RN08, 25 casos mínimos diseñados, retest y regresión.
