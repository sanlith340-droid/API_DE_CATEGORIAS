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