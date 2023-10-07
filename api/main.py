from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

import schemas
from database.config import settings
from database.sessions import engine
from routers import articles

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(
    articles.router,
    prefix=settings.api_prefix,
    tags=['Articles'],
)

origins = [
    'http://localhost:8000',
    'http://localhost:8080',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# @app.on_event('startup')
# async def init_tables():
#     # Disable function if Celery launched
#     SQLModel.metadata.drop_all(engine)
#     SQLModel.metadata.create_all(engine)


@app.get('/')
async def root():
    return {'message': 'Hey'}
