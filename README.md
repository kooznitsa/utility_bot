# Utility bot

## Database structure

![Database structure](https://raw.githubusercontent.com/kooznitsa/utility_bot/main/api/database/db_diagram.png)

## Endpoints

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
| POST	       | / 	                          | Create a user               |
| POST	       | /{user_id}/districts	        | Create a user district      |
| DELETE	    | /{user_id}districts	         | Delete all user districts   |

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