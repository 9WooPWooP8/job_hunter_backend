Бэкенд для проекта по ПИ.

Python3.11

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

baza v dokere!!!!

docker run -p 5432:5432 -e POSTGRES PASSWORD="postgres" -e POSTGRES DB="jobhunter" postgres

uvicorn --reload --proxy-headers --host localhost --port 8000 src.main:app
