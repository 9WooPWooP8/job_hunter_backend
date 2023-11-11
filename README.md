Бэкенд для проекта по ПИ.

Python3.11

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

docker run -p 5432:5432 -e POSTGRES PASSWORD="postgres" -e POSTGRES DB="jobhunter" postgres

cp .env.example .env

uvicorn --reload --proxy-headers --host localhost --port 8000 src.main:app

create migrations:
alembic revision --autogenerate -m "migration comment"

apply migrations:
alembic upgrade head

-----------------------
Docker compose

cp .env.example .env

docker compose up
