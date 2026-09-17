# Registro de defectos

Los siguientes defectos fueron detectados al comparar la versión inicial con el contrato del PDF y se corrigieron en esta versión.

| ID | Defecto y requisito | Severidad / prioridad | Estado | Evidencia y resolución |
|---|---|---|---|---|
| DEF-M4-001 | `GET /products` respondía 405 por estar registrado solo `/products/` (RF06). | Alta / Alta | Cerrado | Se registró la ruta exacta `/products`; retest aprobado. |
| DEF-M4-002 | Faltaba `PUT /products/{id}` (RF09/RF10). | Alta / Alta | Cerrado | Se implementó actualización completa y 404 para ID inexistente. |
| DEF-M4-003 | DELETE de producto respondía 200 con cuerpo (RF11). | Alta / Alta | Cerrado | Ahora responde 204 sin cuerpo. |
| DEF-M4-004 | Producto aceptaba categoría textual libre en vez de `category_id` (RF05/RN06). | Crítica / Alta | Cerrado | Se cambió el esquema y se valida existencia de la categoría. |
| DEF-M4-005 | Se permitían categorías duplicadas ignorando mayúsculas (RN02). | Alta / Alta | Cerrado | Se agregó comparación `casefold()` y respuesta 409. |
| DEF-M4-006 | Límites de nombres no coincidían con RN01/RN03. | Media / Media | Cerrado | Categoría: 3–60; producto: 3–80. |

## Retest y regresión

Cada caso que reproducía un defecto fue reejecutado después de la corrección. Luego se ejecutó la suite completa para regresión. No se deben declarar defectos abiertos sin una nueva evidencia de ejecución.
