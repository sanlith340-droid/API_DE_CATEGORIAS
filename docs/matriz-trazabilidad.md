# Matriz de trazabilidad

| ID | Requisito o regla | Casos relacionados | Cobertura |
|---|---|---|---|
| RF01 | Crear categoría válida | CP-CAT-01 | Cubierto |
| RF02 | Listar categorías | CP-CAT-02 | Cubierto |
| RF03 | Consultar categoría existente | CP-CAT-03 | Cubierto |
| RF04 | Consultar categoría inexistente devuelve 404 | CP-CAT-04 | Cubierto |
| RF05 | Crear producto con categoría existente | CP-PROD-01 | Cubierto |
| RF06 | Listar productos | CP-PROD-02 | Cubierto |
| RF07 | Consultar producto existente | CP-PROD-03 | Cubierto |
| RF08 | Consultar producto inexistente devuelve 404 | CP-PROD-04 | Cubierto |
| RF09 | Actualizar producto válido | CP-PROD-05 | Cubierto |
| RF10 | Actualizar producto inexistente devuelve 404 | CP-PROD-06 | Cubierto |
| RF11 | Eliminar producto existente | CP-PROD-07 | Cubierto |
| RF12 | Eliminar producto inexistente devuelve 404 | CP-PROD-08 | Cubierto |
| RN01 | Nombre de categoría entre 3 y 60 | CP-CAT-05, CP-CAT-06, CP-CAT-07 | Cubierto |
| RN02 | Nombre de categoría único sin distinguir mayúsculas | CP-CAT-08 | Cubierto |
| RN03 | Nombre de producto entre 3 y 80 | CP-PROD-09, CP-PROD-10 | Cubierto |
| RN04 | Precio estrictamente mayor que 0 | CP-PROD-11, CP-PROD-12, CP-PROD-13 | Cubierto |
| RN05 | Stock mayor o igual que 0 | CP-PROD-14, CP-PROD-15 | Cubierto |
| RN06 | `category_id` debe existir | CP-PROD-16, CP-PROD-18 | Cubierto |
| RN07 | Stock igual a 0 se acepta | CP-PROD-14 | Cubierto |
| RN08 | Actualización mantiene validaciones de creación | CP-PROD-17, CP-PROD-18 | Cubierto |

**Resumen:** 20 requisitos/reglas trazados; 25 casos mínimos diseñados; automatización representativa en `test/`.
