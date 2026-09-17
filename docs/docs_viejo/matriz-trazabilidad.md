# Matriz de Trazabilidad

Relaciona cada requisito funcional (RF) y regla de negocio (RN) del
alcance con los casos de prueba (CP para productos, CA para categorías)
que los verifican. El estado indica si el caso ya está automatizado en
`test/` o si es una brecha identificada durante este ciclo.

## Requisitos funcionales — Productos

| ID requisito | Requisito | Caso(s) relacionado(s) | Estado |
|---|---|---|---|
| RF01 | Crear producto | CP001, CP002, CP003, CP005, CP006 | CP001–CP002 automatizados; CP003, CP005, CP006 pendientes |
| RF02 | Consultar productos (listado y filtros) | CP007, CP008, CP009 | Automatizados (fallando por DEF-001) |
| RF03 | Consultar producto por ID | CP010, CP011, CP012 | Automatizados |
| RF04 | Actualizar producto | CP013, CP014, CP015 | Automatizados (CP013/CP015 fallando por DEF-002) |
| RF05 | Eliminar producto | CP016, CP017 | CP016 automatizado (fallando por DEF-003); CP017 pendiente |

## Reglas de negocio — Productos

| ID requisito | Regla | Caso(s) relacionado(s) | Estado |
|---|---|---|---|
| RN01 | El nombre del producto es obligatorio (2–100 caracteres) | CP005, CP006 | Pendientes de automatizar |
| RN02 | El precio debe ser mayor que cero | CP002 | Automatizado |
| RN03 | El stock no puede ser negativo | CP003, CP004 | Pendientes de automatizar |
| RN04 | No se debe devolver como válido un producto inexistente | CP011 | Automatizado |
| RN05 | No se debe eliminar un producto inexistente | CP017 | Pendiente de automatizar |

## Requisitos funcionales — Categorías

| ID requisito | Requisito | Caso(s) relacionado(s) | Estado |
|---|---|---|---|
| RF06 | Crear categoría | CA05, CA06, CA07 | Automatizados |
| RF07 | Consultar categorías (listado y filtros) | CA01, CA12, CA13, CA14 | Automatizados |
| RF08 | Consultar categoría por ID | CA02, CA03, CA04 | Automatizados |
| RF09 | Actualizar categoría | CA08, CA09 | Automatizados |
| RF10 | Eliminar categoría | CA10, CA11 | Automatizados |

## Reglas de negocio — Categorías

| ID requisito | Regla | Caso(s) relacionado(s) | Estado |
|---|---|---|---|
| RN06 | El nombre de la categoría es obligatorio (3–50 caracteres) | CA06, CA07 | Automatizados |
| RN07 | No se debe devolver como válida una categoría inexistente | CA03 | Automatizado |
| RN08 | No se debe eliminar una categoría inexistente | CA11 | Automatizado |

## Brechas de cobertura detectadas

Al construir esta matriz se identificaron los siguientes huecos, que se
documentan en `casos-prueba.md` como casos pendientes de automatizar:

- **RN01 / RN03 (productos):** no existía un test que probara nombre
  vacío/corto ni stock negativo/frontera directamente sobre `POST
  /products`; solo se cubría el precio negativo.
- **RF05 / RN05 (productos):** no existía un caso para `DELETE
  /products/{id}` con un ID inexistente (sí existe su equivalente para
  categorías, CA11).

Ningún requisito del alcance quedó sin al menos un caso asociado, ya sea
automatizado o documentado como pendiente.
