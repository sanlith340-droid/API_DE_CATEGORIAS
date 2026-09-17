# Casos de prueba

Todos los casos usan el fixture de reinicio de datos. **Resultado obtenido:** PASS después de la corrección. Los casos automatizados están implementados en `test/test_categories.py` y `test/test_products.py`.

| ID | Requisito | Título / tipo | Prioridad | Precondición y datos | Pasos | Esperado / obtenido |
|---|---|---|---:|---|---|---|
| CP-CAT-01 | RF01 | Crear categoría válida / positiva | Alta | API activa; `Periféricos` | POST `/categories` | 201 y objeto / PASS |
| CP-CAT-02 | RF02 | Listar categorías / positiva | Media | Datos base | GET `/categories` | 200 y lista / PASS |
| CP-CAT-03 | RF03 | Consultar existente / positiva | Media | ID 1 | GET `/categories/1` | 200 / PASS |
| CP-CAT-04 | RF04 | Consultar inexistente / negativa | Alta | ID 99999 | GET `/categories/99999` | 404 / PASS |
| CP-CAT-05 | RN01 | Nombre de 2 / frontera negativa | Alta | `AB` | POST `/categories` | 422 / PASS |
| CP-CAT-06 | RN01 | Nombre de 3 / frontera positiva | Media | `Red` | POST `/categories` | 201 / PASS |
| CP-CAT-07 | RN01 | Nombre de 60 / frontera positiva | Media | 60 caracteres | POST `/categories` | 201 / PASS |
| CP-CAT-08 | RN02 | Duplicado case-insensitive / negativa | Alta | `audio` existente como `Audio` | POST `/categories` | 409 / PASS |
| CP-PROD-01 | RF05 | Crear producto válido / positiva | Alta | Producto y categoría 1 | POST `/products` | 201 / PASS |
| CP-PROD-02 | RF06 | Listar productos / positiva | Media | Datos base | GET `/products` | 200 / PASS |
| CP-PROD-03 | RF07 | Consultar producto existente / positiva | Media | ID 1 | GET `/products/1` | 200 / PASS |
| CP-PROD-04 | RF08 | Consultar inexistente / negativa | Alta | ID 99999 | GET `/products/99999` | 404 / PASS |
| CP-PROD-05 | RF09 | Actualizar válido / positiva | Alta | Body válido | PUT `/products/1` | 200 y cambios / PASS |
| CP-PROD-06 | RF10 | Actualizar inexistente / negativa | Alta | ID 99999 | PUT `/products/99999` | 404 / PASS |
| CP-PROD-07 | RF11 | Eliminar existente / positiva | Alta | ID 1 | DELETE `/products/1` | 204 sin cuerpo / PASS |
| CP-PROD-08 | RF12 | Eliminar inexistente / negativa | Alta | ID 99999 | DELETE `/products/99999` | 404 / PASS |
| CP-PROD-09 | RN03 | Nombre de 2 / frontera negativa | Alta | `AB` | POST `/products` | 422 / PASS |
| CP-PROD-10 | RN03 | Nombre de 3 / frontera positiva | Media | `RAM` | POST `/products` | 201 / PASS |
| CP-PROD-11 | RN04 | Precio 0 / frontera negativa | Alta | `price=0` | POST `/products` | 422 / PASS |
| CP-PROD-12 | RN04 | Precio negativo / negativa | Alta | `price=-1000` | POST `/products` | 422 / PASS |
| CP-PROD-13 | RN04 | Precio mínimo positivo / frontera | Media | `price=0.01` | POST `/products` | 201 / PASS |
| CP-PROD-14 | RN05/RN07 | Stock 0 / frontera positiva | Alta | `stock=0` | POST `/products` | 201 / PASS |
| CP-PROD-15 | RN05 | Stock negativo / negativa | Alta | `stock=-1` | POST `/products` | 422 / PASS |
| CP-PROD-16 | RN06 | Categoría inexistente al crear | Alta | `category_id=99999` | POST `/products` | 404 / PASS |
| CP-PROD-17 | RN08 | Precio inválido al actualizar | Alta | `price=0` | PUT `/products/1` | 422 / PASS |
| CP-PROD-18 | RN06/RN08 | Categoría inválida al actualizar | Alta | `category_id=99999` | PUT `/products/1` | 404 / PASS |

## Ejecución

Los 25 casos están representados por pruebas automatizadas o por escenarios equivalentes dentro de la suite. El resultado final debe confirmarse con `python -m pytest -v`; el informe de ejecución registra la evidencia numérica.
