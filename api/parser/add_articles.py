from time import sleep

from sqlmodel.ext.asyncio.session import AsyncSession

from database.sessions import async_engine
from parser.parser import Page, Article
from repositories.articles import ArticleRepository
from repositories.tags import TagRepository
from repositories.districts import DistrictRepository


async def add_articles() -> None:
    async with AsyncSession(async_engine) as async_session:
        article_repo = ArticleRepository(async_session)
        tag_repo = TagRepository(async_session)
        district_repo = DistrictRepository(async_session)

        page = Page('https://gradskeinfo.rs/kategorija/servisne-info/')

        for i in page.get_urls():
            article = Article(i)
            article_created = await article_repo.create(article.get_items())
            print(f'Article ID={article_created.id} items added to database')

            for tag in article.get_tags():
                await tag_repo.create(article_created.id, tag)
            print('Tags added to database')

            for district in article.get_districts():
                await district_repo.create(article_created.id, district)
            print('Districts added to database')

            sleep(3)
