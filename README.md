# Utility bot

A Telegram bot that sends updates on water and electricity disruptions/outage in Novi Sad and its vicinity (Serbia).

## Tech stack

<img src="https://img.shields.io/badge/FastAPI-fc884d?style=for-the-badge&logo=fastapi&logoColor=black"/> <img src="https://img.shields.io/badge/Redis-fc884d?style=for-the-badge&logo=Redis&logoColor=black"/> <img src="https://img.shields.io/badge/Celery-fc884d?style=for-the-badge"/> <img src="https://img.shields.io/badge/PostgreSQL-f5df66?style=for-the-badge&logo=PostgreSQL&logoColor=black"/> <img src="https://img.shields.io/badge/AsyncIO-65a362?style=for-the-badge&logo=AsyncIO&logoColor=black"/> <img src="https://img.shields.io/badge/aiogram-65a362?style=for-the-badge&logo=aiogram&logoColor=black"/>

## App structure

- API (FastAPI): 
  - Scrapes latest articles from https://gradskeinfo.rs/kategorija/servisne-info/
  - Sends data to the database and endpoints
- Bot (aiogram):
  - Sends a new user to the API endpoint /users
  - Sends districts chosen by the user to the API endpoint /users/{user_id}/districts
  - Receives user articles from the API endpoint /users/{user_id}/articles
  - Sends messages to users on schedule

## Database structure

![Database structure](https://raw.githubusercontent.com/kooznitsa/utility_bot/main/api/database/db_diagram.png)

## API endpoints

| Method      | Endpoint                     | Description                 |
|-------------|------------------------------|-----------------------------|
| ---GENERAL  | /	                           |                             |
| GET	        | /	                           | Root                        |
| GET	        | /docs	                       | Documentation               |
| ---ARTICLES | /api/articles                | Articles                    | 
| GET         | /                            | Get all articles            |
| GET         | ?district={d1}&district={d2} | Get articles with districts |
| POST        | /                            | Create an article           |
| DELETE      | /{article_id}                | Delete an article           |
| ---USERS	   | /api/users                   | Users                       |
| GET	        | /                            | Get all users               |
| POST	       | / 	                          | Create a user               |
| GET	        | /{user_id}	                  | Get a user                  |
| DELETE	     | /{user_id}	                  | Delete a user               |
| POST	       | /{user_id}/districts	        | Create a user district      |
| POST	       | /{user_id}districts/delete	  | Delete all user districts   |
| GET	        | /{user_id}/articles	         | Get user articles           |

## Commands

### With Docker

#### Commands to start up the project

- Create network: ```docker network create my-net```
- Build Docker containers: ```docker-compose up -d --build```

#### List of all commands

- Docker:
  - Create network: ```docker network create my-net```
  - Build Docker containers: ```docker-compose up -d --build```
  - Remove Docker containers: ```docker-compose down```
  - Bring down the existing containers and volumes: ```docker-compose down -v```

- Alembic:
  - Initialize Alembic: ```docker exec -it fastapi_service poetry run alembic init -t async migrations```
  - Generate a migration file: ```docker exec -it fastapi_service poetry run alembic revision --autogenerate -m "init"```
  - Apply the migration: ```docker exec -it fastapi_service poetry run alembic upgrade head```

- Database:
  - Display a table: ```docker exec -it db_postgres psql -U postgres utility_db -c "SELECT * FROM public.articles"```

### Without Docker

**1. Edit .env**
```
| With Docker                                              | Without Docker                                 |
|----------------------------------------------------------|------------------------------------------------|
| POSTGRES_SERVER=db_potgres                               | POSTGRES_SERVER=localhost                      |
| CELERY_BROKER_URL='redis://redis:6379'                   | CELERY_BROKER_URL='redis://127.0.0.1:6379'     |
| CELERY_RESULT_BACKEND='redis://redis:6379'               | CELERY_RESULT_BACKEND='redis://127.0.0.1:6379' |
| REDIS_URL='redis://redis:6379'                           | REDIS_URL='redis://127.0.0.1:6379'             |
| GW_ROOT_URL='fastapi_service://fastapi_service:8000/api' | GW_ROOT_URL='http://127.0.0.1:8000/api'        |
```

**2. Create utility_db database (PostgreSQL 16)**

**3. Start Redis server in Ubuntu terminal**
```
# Once:
sudo add-apt-repository universe
sudo apt install redis
sudo service redis-service restart

# Always:
sudo service redis-server start
sudo service redis-server status
# Status: "Ready to accept connections"
redis-cli
```

**4. Start uvicorn server (API)**
```
cd api

py -m venv venv
venv\Scripts\activate
# If venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system, run:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

py -m pip install poetry
py -m poetry install

py -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

**5. Run Alembic migrations**
```
python -m alembic stamp head
python -m alembic upgrade head
```

**6. Launch Celery (separate terminal tabs)**
```
# Tab1: 
cd api
venv\Scripts\activate
py -m celery -A parser.tasks worker --pool=solo -l info -Q main-queue -c 1

# Tab2:
cd api
venv\Scripts\activate
py -m celery -A parser.tasks beat --loglevel=info
```

**7. Launch bot (separate terminal tab)**
```
cd bot

py -m venv venv
venv\Scripts\activate

py -m pip install poetry
py -m poetry install

py main.py
```
