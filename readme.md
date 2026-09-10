## MODULO 3 SANTIAGO

python -m venv .venv

.venv\Scripts\Activate.ps1 

python -m pip install fastapi

python -m pip install "uvicorn[standard]"

python -m pip install pytest httpx

python -m pip freeze > requirements.txt

python -m pip install -r requirements.txt

## INCIAR SERVER 

python -m uvicorn app.main:app --reload

http://127.0.0.1:8000/docs


## DOCUMENTACION DEL PROYECTO 3 CATEGORIAS

Tecnologías // 
Python · 
FastAPI · 
Pydantic · 
pytest · 
TestClient · 


## Producto API REST de categorías + suite de pruebas automatizadas 

Propósito: Aplicar de manera autónoma los conceptos de FastAPI 
aprendidos en el Módulo III mediante la construcción y prueba de un 
CRUD de categorías.

1. Competencia a desarrollar // ✅

Construir y verificar una API REST básica 
con FastAPI, 
aplicando modelos Pydantic, 
validaciones, 
códigos HTTP, 
manejo de errores, 
filtros y 
pruebas automatizadas.

2. Contexto de la actividad // ✅

Una tienda tecnológica necesita administrar las categorías utilizadas para clasificar sus productos. 

Debes implementar un servicio REST denominado API de Categorías. 
En esta actividad no se utilizará una base de datos real: 
los datos se almacenarán temporalmente en memoria para concentrar el trabajo en el comportamiento de la API y sus pruebas.


3. Requerimiento funcional Cada categoría debe manejar la siguiente información:

