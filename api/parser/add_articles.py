from time import sleep

from sqlmodel.ext.asyncio.session import AsyncSession

from database.sessions import async_engine
from parser.parser import Page, Article
from repositories.articles import ArticleRepository
from repositories.districts import DistrictRepository


class ItemIterator:
    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            item = next(self._items)
        except StopIteration:
            raise StopAsyncIteration
        return item


class ArticleIterator:
    def __init__(self, urls):
        self._urls = iter(urls)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            url = next(self._urls)
        except StopIteration:
            raise StopAsyncIteration

        async with AsyncSession(async_engine) as async_session:
            article_repo = ArticleRepository(async_session)
            district_repo = DistrictRepository(async_session)

            article = Article(url)
            if article_created := await article_repo.create(article.get_items()):
                article_id = article_created.id

                async for district in ItemIterator(article.get_districts()):
                    await district_repo.create(article_id, district)

                return article_id


async def add_articles():
    page = Page('https://gradskeinfo.rs/kategorija/servisne-info/')

    async for article_id in ArticleIterator(page.get_urls()):
        if article_id:
            print(f'Article ID={article_id} added to database')
        else:
            print('Article already in database')
        sleep(3)
