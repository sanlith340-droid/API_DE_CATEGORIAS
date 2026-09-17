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

## Auditoría

La carpeta `docs/` contiene:

- `plan-pruebas.md`
- `matriz-trazabilidad.md`
- `casos-prueba.md`
- `registro-defectos.md`
- `informe-ejecucion.md`

La auditoría cubre RF01–RF12, RN01–RN08, 25 casos mínimos diseñados, retest y regresión.
