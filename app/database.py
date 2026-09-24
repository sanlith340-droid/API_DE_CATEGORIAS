# "Base de datos" en memoria: listas de diccionarios (se pierde al reiniciar).
# Es intencional: el foco es el comportamiento HTTP, no la persistencia.
# Los tests reinician estas listas antes de cada prueba (fixture reset_db).
# Coinciden con los "datos de prueba base" del plan: Periféricos, Audio,
# Mouse inalámbrico (120000 / stock 5) y Monitor (850000 / stock 0 → frontera RN07).

# description y active son sobrantes del Módulo III: Category no los expone.
categories_db: list[dict] = [
    {"id": 1, "name": "Periféricos", "description": "Accesorios tecnológicos", "active": True},
    {"id": 2, "name": "Audio", "description": "Equipos de sonido", "active": True},
]

products_db: list[dict] = [
    {"id": 1, "name": "Mouse inalámbrico", "price": 120000.0, "stock": 5, "category_id": 1},
    {"id": 2, "name": "Monitor", "price": 850000.0, "stock": 0, "category_id": 1},
]
