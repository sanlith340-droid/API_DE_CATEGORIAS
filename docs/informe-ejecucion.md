# Informe de Ejecución de Pruebas

Proyecto: Products API (productos + categorías)
Versión: 1.0.0
Fecha: Septiembre de 2026
Responsable: Santiago Buitrago Goyeneche
Comando ejecutado: `python -m pytest -v` (entorno: Python 3.12, pytest 8.4.2)

## 1. Resumen

Casos diseñados (documentados en `casos-prueba.md`): 32
Casos automatizados y ejecutados: 27
Casos documentados, pendientes de automatizar: 5 (CP003, CP004, CP005,
CP006, CP017)
Aprobados: 21
Fallidos: 6
Bloqueados: 0

## 2. Detalle de fallos

| Test | Requisito | Defecto |
|---|---|---|
| `test_get_products` | RF02 | DEF-001 |
| `test_filter_available_products` | RF02 | DEF-001 |
| `test_filter_products_by_category` | RF02 | DEF-001 |
| `test_update_product` | RF04 | DEF-002 |
| `test_update_non_existing_product` | RF04 | DEF-002 |
| `test_delete_product` | RF05 | DEF-003 |

Los 6 fallos se explican completamente por los 3 defectos registrados en
`registro-defectos.md`; no se detectaron fallos adicionales no
relacionados con un defecto conocido.

## 3. Métricas

Tasa de aprobación = aprobados / ejecutados × 100 = 21 / 27 × 100 = **77.8 %**
Tasa de fallos = fallidos / ejecutados × 100 = 6 / 27 × 100 = **22.2 %**
Cobertura de ejecución = ejecutados / diseñados × 100 = 27 / 32 × 100 = **84.4 %**

Defectos críticos abiertos: 0
Defectos altos abiertos: 2 (DEF-001, DEF-002)
Defectos medios abiertos: 1 (DEF-003)

## 4. Defectos relevantes

- **DEF-001** (Alta/Alta): `GET /products` sin barra final responde 405
  en lugar de 200; afecta el listado y sus filtros.
- **DEF-002** (Alta/Alta): `PUT /products/{id}` no está implementado
  (solo existe `PATCH`); rompe la actualización completa esperada por
  cualquier cliente REST estándar.
- **DEF-003** (Media/Media): `DELETE /products/{id}` devuelve 200 con
  cuerpo en vez de 204 sin cuerpo, inconsistente con el mismo endpoint
  ya implementado correctamente en categorías.

## 5. Comparación contra criterios de salida

| Criterio (definido en `plan-pruebas.md`) | Resultado real | Estado |
|---|---|---|
| 100 % de los casos críticos ejecutados | CP002 ejecutado (PASSED); CP003 (crítico, stock negativo) aún no automatizado | **NO CUMPLIDO** |
| 0 defectos críticos abiertos ligados a reglas de negocio (precio, stock, nombre obligatorio) | Los 3 defectos abiertos son de contrato HTTP, no de reglas de negocio | Cumplido |
| Al menos 90 % de los casos totales aprobados | 77.8 % | **NO CUMPLIDO** |
| Inconsistencias de contrato HTTP (R03/R04/R06 del plan) quedan registradas | DEF-001, DEF-002, DEF-003 documentados con pasos reproducibles | Cumplido |

## 6. Conclusión técnica

El ciclo **no cumple todavía** los criterios de salida definidos en el
plan de pruebas. Aunque las reglas de negocio centrales sobre productos
(`price > 0`, validación de tipos) y todo el CRUD de categorías están
correctamente implementados y verificados (14/14 casos de categorías
aprobados), el módulo de productos presenta tres defectos de contrato
HTTP que degradan la tasa de aprobación general por debajo del 90 %
requerido: la falta de soporte para consultas sin barra final en el
listado (DEF-001), la ausencia del verbo `PUT` para actualización
completa (DEF-002) y un código de retorno inconsistente en el borrado
(DEF-003).

Antes de cerrar el ciclo se debe: (1) corregir DEF-001, DEF-002 y
DEF-003; (2) ejecutar retest de los seis casos afectados; (3) ejecutar
regresión completa (`pytest -v`) para confirmar que ninguna corrección
introdujo efectos secundarios; y (4) automatizar los cinco casos
pendientes (CP003, CP004, CP005, CP006, CP017) para elevar la cobertura
de ejecución del 84.4 % actual al 100 % de lo diseñado.

Una tasa de aprobación alta por sí sola no garantiza el cierre del
ciclo: en este caso, incluso si se alcanzara el 90 % exigido, el
criterio de "100 % de casos críticos ejecutados" seguiría sin cumplirse
mientras existan casos críticos (como CP003) documentados pero no
automatizados, ya que un caso no ejecutado no aporta evidencia real de
que el sistema cumple la regla de negocio que dice cubrir.
