Pasos para instalacion:

pip install fastapi uvicorn sqlalchemy pydantic
python -m venv venv

    ESTO SE DEBE DE HACER SIEMPRE:

.\venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic

cd app
uvicorn main:app --reload
cd ..

Para conectar con el postgres:
pip install psycopg2-binary
http://127.0.0.1:8000/docs
------------------------------
python -m venv venv (Crear la caja)

.\venv\Scripts\activate (Entrar a la caja)

pip install fastapi uvicorn sqlalchemy pydantic psycopg2-binary (Llenar la caja)
pip install pydantic-settings python-dotenv
uvicorn main:app --reload (Arrancar)