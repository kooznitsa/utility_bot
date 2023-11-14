from __future__ import absolute_import

import asyncio

from celery import Celery
from celery.schedules import crontab

from .manager import add_articles, delete_articles
from database.config import settings

celery_app = Celery(
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['application/json'],
    result_serializer='json',
    beat_schedule={
        'scrape-articles-scheduled-task': {
            'task': 'parser.tasks.scrape_articles',
            'schedule': crontab(minute=0, hour='8-20', day_of_week='mon-fri'),
        },
        'remove-articles-scheduled-task': {
            'task': 'parser.tasks.remove_articles',
            'schedule': crontab(minute=1, hour=1),
        }
    },
    task_routes={
        'parser.tasks.scrape_articles': 'main-queue',
        'parser.tasks.remove_articles': 'main-queue',
    },
    timezone=settings.timezone,
    enable_utc=True,
)


@celery_app.task
def scrape_articles():
    asyncio.get_event_loop().run_until_complete(add_articles())


@celery_app.task
def remove_articles():
    asyncio.get_event_loop().run_until_complete(delete_articles())
