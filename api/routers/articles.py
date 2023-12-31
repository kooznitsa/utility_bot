from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security.api_key import APIKey

from .protected import get_api_key
from database.errors import EntityDoesNotExist
from database.sessions import get_repository
from repositories.articles import ArticleRepository
from schemas.articles import Article, ArticleCreate, ArticleRead


router = APIRouter(prefix='/articles')


@router.get(
    '/',
    response_model=list[Optional[ArticleRead]],
    status_code=status.HTTP_200_OK,
    name='get_articles',
)
async def get_articles(
    district: Optional[list[str]] = Query(default=None),
    limit: int = Query(default=50, lte=100),
    offset: int = Query(default=0),
    repository: ArticleRepository = Depends(get_repository(ArticleRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> list[Optional[ArticleRead]]:
    return await repository.list(
        district=district,
        limit=limit,
        offset=offset,
    )


@router.get(
    '/{article_id}',
    response_model=ArticleRead,
    status_code=status.HTTP_200_OK,
    name='get_article',
)
async def get_article(
    article_id: int,
    repository: ArticleRepository = Depends(get_repository(ArticleRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> ArticleRead:
    try:
        result = await repository.get(model_id=article_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Article with ID={article_id} not found'
        )
    return result


@router.delete(
    '/{article_id}',
    status_code=status.HTTP_200_OK,
    name='delete_article',
)
async def delete_article(
    article_id: int,
    repository: ArticleRepository = Depends(get_repository(ArticleRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> None:
    try:
        await repository.get(model_id=article_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Article with ID={article_id} not found'
        )
    return await repository.delete(model=Article, model_id=article_id)
