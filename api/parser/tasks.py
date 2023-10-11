from __future__ import absolute_import

import asyncio
from dotenv import load_dotenv
import os

from celery import Celery
from celery.schedules import crontab

from .add_articles import add_articles

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
        'send-messages-scheduled-task': {
            'task': 'parser.tasks.scrape_articles',
            'schedule': crontab(minute='*/60')
        }
    },
    task_routes={
        'parser.tasks.scrape_articles': 'main-queue',
    },
)


@celery_app.task
def scrape_articles():
    asyncio.get_event_loop().run_until_complete(add_articles())
