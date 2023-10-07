Create network: ```docker network create my-net```

Start Redis server: ```redis-server --save 20 1 --loglevel warning```

Launch Celery tasks: ```poetry run celery -A parser.tasks worker --beat -l info -Q main-queue -c 1```

Launch Uvicorn: ```uvicorn main:app --reload```

Build Docker containers: ```docker-compose up -d --build```