# Utility bot

## Database structure

![Database structure](https://raw.githubusercontent.com/kooznitsa/utility_bot/main/api/database/db_diagram.png)

## Commands

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