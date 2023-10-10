# Utility bot

## Database structure

![Database structure](https://raw.githubusercontent.com/kooznitsa/utility_bot/main/api/database/db_diagram.png)

## Commands

1. Create network: ```docker network create my-net```

2. Start Redis server: ```redis-server --save 20 1 --loglevel warning```

3. Launch Celery tasks: ```poetry run celery -A parser.tasks worker --beat -l info -Q main-queue -c 1```

4. Launch Uvicorn: ```uvicorn main:app --reload```

5. Build Docker containers: ```docker-compose up -d --build```

6. Remove Docker containers: ```docker-compose down```

Commands 2–4: if not using Docker.