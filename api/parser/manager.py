from sqlmodel.ext.asyncio.session import AsyncSession

from database.sessions import async_engine
from parser.parser import Page, Article
from repositories.articles import ArticleRepository
from repositories.districts import DistrictRepository
from schemas.articles import Article as ArticleSchema
from utils.async_iterator import AsyncItemIterator


async def add_articles():
    page = Page('https://gradskeinfo.rs/kategorija/servisne-info/')

    async for url in AsyncItemIterator(page.get_urls()):
        async with AsyncSession(async_engine) as async_session:
            article_repo = ArticleRepository(async_session)
            district_repo = DistrictRepository(async_session)

            article = Article(url)

            if article_created := await article_repo.create(article.get_items()):
                article_id = article_created.id

                async for district in AsyncItemIterator(article.get_districts()):
                    await district_repo.create(article_id, district, ArticleSchema)

                print(f'Article ID={article_id} added to database')
            else:
                print('Article already in database')


async def delete_articles():
    async with AsyncSession(async_engine) as async_session:
        article_repo = ArticleRepository(async_session)
        await article_repo.delete_bunch()
