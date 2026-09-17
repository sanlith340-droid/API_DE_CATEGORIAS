# Plan de pruebas — TechStore API

## Identificación

**Versión auditada:** 1.0.0  
**Responsable:** Santiago Buitrago Goyeneche  
**Tecnologías:** Python, FastAPI, Pydantic, pytest y TestClient.  
**Fecha:** septiembre de 2026.

## Objetivo y alcance

Verificar que la API cumpla EP01–EP08, RF01–RF12 y RN01–RN08 del PDF del Mini Proyecto Evaluable del Módulo IV. Se cubren creación, listado, consulta, actualización, eliminación, errores 404/409/422 y valores frontera.

Incluido: `POST/GET /categories`, `GET /categories/{id}`, `POST/GET /products`, `GET /products/{id}`, `PUT /products/{id}`, `DELETE /products/{id}`, además de `PATCH` como extensión útil. Fuera de alcance: autenticación, autorización, rendimiento, seguridad especializada, UI y persistencia real.

## Estrategia

Se aplican pruebas funcionales positivas, negativas y de frontera. Los datos se almacenan en listas en memoria y cada prueba reinicia ambas listas mediante fixtures. La suite automatizada contiene casos de categorías y productos, incluidos duplicados, límites de longitud, precio, stock, categoría inexistente, actualización y eliminación.

## Riesgos priorizados

| ID | Riesgo | Probabilidad | Impacto | Prioridad |
|---|---|---:|---:|---:|
| R01 | Producto con categoría inexistente | Media | Alto | Alta |
| R02 | Categorías duplicadas por capitalización | Alta | Alto | Alta |
| R03 | Precio cero/negativo aceptado | Alta | Alto | Alta |
| R04 | Stock negativo aceptado | Media | Alto | Alta |
| R05 | Verbo o código HTTP incorrecto | Media | Alto | Alta |
| R06 | Límites de nombres incorrectos | Media | Medio | Media |

## Ambiente y datos

Python 3.12+, FastAPI, pytest, HTTPX/TestClient y sistema Linux o Windows. Datos base: categorías `Periféricos` y `Audio`; productos `Mouse inalámbrico` (120000, stock 5) y `Monitor` (850000, stock 0); ID inexistente 99999; precios 0, -1000 y 0.01; stock -1 y 0.

## Criterios de entrada, suspensión y salida

Entrada: dependencias instaladas, módulos importables y contrato definido. Suspender si la aplicación no inicia o no se puede ejecutar ningún caso crítico. Reanudar después de corregir el bloqueo y realizar retest. Salida: 100% de casos críticos ejecutados, 100% de pruebas automatizadas aprobadas, cero defectos críticos/altos abiertos y retest/regresión documentados.

**Responsable de ejecución:** Santiago Buitrago Goyeneche.  
**Evidencia:** salida de `python -m pytest -v`, casos, matriz y registro de defectos.
