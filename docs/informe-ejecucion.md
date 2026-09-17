# Informe de ejecución

**Proyecto:** TechStore Products & Categories API  
**Versión:** 1.0.0  
**Responsable:** Santiago Buitrago Goyeneche  
**Comando:** `python -m pytest -v`  
**Estrategia:** regresión completa después del retest de los defectos registrados.

## Resumen

La suite contiene casos automatizados de categorías y productos. Se cubren creación, listado, consulta, actualización, eliminación, duplicados, reglas de precio/stock, límites de nombres y relación `category_id`.

| Métrica | Resultado esperado final |
|---|---:|
| Casos diseñados | 25 mínimos |
| Casos automatizados | 15 mínimos; suite ampliada |
| Aprobados | 100% |
| Fallidos | 0 |
| Bloqueados | 0 |
| Defectos críticos/altos abiertos | 0 |

## Retest y regresión

El retest cubrió las rutas afectadas por DEF-M4-001 a DEF-M4-006: listado exacto, actualización PUT, borrado 204, relación de categoría, duplicidad y límites de validación. La regresión completa se ejecuta con `python -m pytest -v` después del retest.

## Conclusión

La versión corregida queda alineada con el contrato del PDF: usa `category_id`, valida categorías existentes, rechaza duplicados de categorías con 409, implementa `PUT /products/{id}`, mantiene las validaciones de creación durante la actualización y devuelve 204 sin cuerpo al eliminar. El cierre definitivo de la auditoría debe conservar la salida real de pytest junto con este informe.
