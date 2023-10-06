from __future__ import absolute_import

import os
from dotenv import load_dotenv
from time import sleep

import asyncio
from celery import Celery
from celery.schedules import crontab
from sqlmodel.ext.asyncio.session import AsyncSession

from database.sessions import async_engine
from repositories.tags import TagRepository
from repositories.districts import DistrictRepository
from repositories.articles import ArticleRepository
from parser.parser import Page, Article

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
            'schedule': crontab(minute='*/1')
        }
    },
    task_routes={
        'parser.tasks.scrape_articles': 'main-queue',
    },
)


async def scrape_articles() -> None:
    async with AsyncSession(async_engine) as async_session:
        article_repo = ArticleRepository(async_session)
        tag_repo = TagRepository(async_session)
        district_repo = DistrictRepository(async_session)

        page = Page('https://gradskeinfo.rs/kategorija/servisne-info/')

        for i in page.get_urls():
            article = Article(i)
            await article_repo.create(article.get_items())

            for tag in article.get_tags():
                await tag_repo.create(tag)

            for district in article.get_districts():
                await district_repo.create(district)

            sleep(3)


@celery_app.task
def scrape_articles():
    asyncio.get_event_loop().run_until_complete(scrape_articles())
