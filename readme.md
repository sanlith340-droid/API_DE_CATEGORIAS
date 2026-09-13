# Módulo 3 — Santiago Buitrago Goyeneche

Proyecto del curso **Pruebas de Software**, Módulo III: construcción y prueba
de una API REST con FastAPI. El proyecto contiene dos recursos:

- **Productos** (`/products`) — CRUD original de la práctica del módulo.

- **Categorías** (`/categories`) — CRUD que implementa punto por punto la
  *Actividad Autónoma: API de Categorías con FastAPI* 

---

## 1. Instalación

```bash
python -m venv .venv

.venv\Scripts\Activate.ps1

python -m pip install fastapi "uvicorn[standard]" pytest httpx

python.exe -m pip install --upgrade pip

```

(El `requirements.txt` del repo ya trae estas dependencias congeladas con
`pip freeze`, así que también puedes instalar con:)

```bash
python -m pip install -r requirements.txt
```

## 2. Ejecutar el servidor

```bash
python -m uvicorn app.main:app --reload
```

Swagger interactivo disponible en: <http://127.0.0.1:8000/docs>

## 3. Ejecutar las pruebas

```bash
python -m pytest -v.

python -m pytest test/test_categories.py -v

python -m pytest -k "" -v


## 4. API de Categorías (Actividad Autónoma — Módulo III)

**Tecnologías:** Python · FastAPI · Pydantic · pytest · TestClient

**Propósito:** aplicar de manera autónoma los conceptos de FastAPI del
Módulo III mediante la construcción y prueba de un CRUD de categorías, sin
base de datos real (datos en memoria en `app/database.py`).

### 4.1 Modelo de datos

| Campo | Tipo | Obligatorio | Regla principal |
|---|---|---|---|
| `id` | int | Generado | Identificador único, lo asigna el servidor |
| `name` | str | Sí | 3 a 50 caracteres |
| `description` | str \| None | No | Máximo 200 caracteres |
| `active` | bool | No | `true` por defecto |

Ejemplo de JSON:

```json
{
  "id": 1,
  "name": "Computadores",
  "description": "Equipos de cómputo",
  "active": true
}
```

Modelos Pydantic en `app/schemas.py`: `CategoryCreate`, `CategoryUpdate`
(todos los campos opcionales, para PATCH) y `Category` (respuesta, incluye
`id`).

### 4.2 Endpoints

| Método | Endpoint | Función | Código exitoso |
|---|---|---|---|
| GET | `/categories` | Listar categorías | 200 |
| GET | `/categories/{category_id}` | Consultar una categoría | 200 |
| POST | `/categories` | Crear categoría | 201 |
| PATCH | `/categories/{category_id}` | Actualizar parcialmente | 200 |
| DELETE | `/categories/{category_id}` | Eliminar categoría | 204 |
| GET | `/categories?active=true` | Filtrar categorías activas | 200 |
| GET | `/categories?search=comp` | Reto opcional: buscar por nombre (sin distinguir mayúsculas/minúsculas) | 200 |

Reglas de error:

- Categoría inexistente → **404** con `{"detail": "Category not found"}`.
- Datos inválidos (Pydantic los rechaza) → **422**.

### 4.3 Pruebas automatizadas

Ubicadas en `test/test_categories.py`, implementadas con
`fastapi.testclient.TestClient`. Incluyen las 12 pruebas de la matriz de la
actividad (CA01–CA12) más 2 pruebas adicionales para el reto opcional de
búsqueda:

| ID | Escenario | Resultado esperado |
|---|---|---|
| CA01 | Listar categorías | 200 y lista JSON |
| CA02 | Consultar existente | 200 |
| CA03 | Consultar inexistente | 404 |
| CA04 | ID inválido | 422 |
| CA05 | Crear válida | 201 |
| CA06 | Nombre demasiado corto | 422 |
| CA07 | Falta nombre | 422 |
| CA08 | Actualizar existente | 200 |
| CA09 | Actualizar inexistente | 404 |
| CA10 | Eliminar existente | 204 |
| CA11 | Eliminar inexistente | 404 |
| CA12 | Filtrar activas | 200, solo `active=true` |
| extra | Buscar por nombre (con resultado) | 200 |
| extra | Buscar por nombre (sin resultado) | 200, lista vacía |

Se usa un fixture `autouse=True` (`reset_categories_db`) que restablece
`categories_db` antes de cada prueba, garantizando que ninguna prueba dependa
del resultado de otra.

Resultado real de la ejecución (`pytest test/test_categories.py -v`):

```
14 passed, 10 warnings in 0.84s
```

---


