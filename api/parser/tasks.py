from __future__ import absolute_import

import asyncio
from dotenv import load_dotenv
import os

from celery import Celery
from celery.schedules import crontab

from .manager import add_articles, delete_articles

load_dotenv()

celery_app = Celery(
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6379'),
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['application/json'],
    result_serializer='json',
    beat_schedule={
        'scrape-articles-scheduled-task': {
            'task': 'parser.tasks.scrape_articles',
            'schedule': crontab(minute='*/1')
            # 'schedule': crontab(minute=0, hour='*/3,8-19')
        },
        'remove-articles-scheduled-task': {
            'task': 'parser.tasks.remove_articles',
            'schedule': crontab(hour='*/23')
        }
    },
    task_routes={
        'parser.tasks.scrape_articles': 'main-queue',
        'parser.tasks.remove_articles': 'main-queue',
    },
)


@celery_app.task
def scrape_articles():
    asyncio.get_event_loop().run_until_complete(add_articles())


@celery_app.task
def remove_articles():
    asyncio.get_event_loop().run_until_complete(delete_articles())
