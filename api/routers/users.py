from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from fastapi.security.api_key import APIKey

from .protected import get_api_key
from database.errors import EntityDoesNotExist, EntityAlreadyExists
from database.sessions import get_repository
from repositories.users import UserRepository
from repositories.districts import DistrictRepository
from schemas.users import User, UserCreate, UserRead
from schemas.articles import ArticleRead
from schemas.districts import DistrictRead, DistrictCreate


router = APIRouter(prefix='/users')


@router.post(
    '/',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    name='create_user',
)
async def create_user(
    user_create: UserCreate = Body(...),
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> UserRead:
    try:
        return await repository.create(model_create=user_create)
    except EntityAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User with this ID already exists'
        )


@router.get(
    '/',
    response_model=list[Optional[UserRead]],
    status_code=status.HTTP_200_OK,
    name='get_users',
)
async def get_users(
    district: Optional[list[str]] = Query(default=None),
    limit: int = Query(default=50, lte=100),
    offset: int = Query(default=0),
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> list[Optional[UserRead]]:
    return await repository.list_users(
        district=district,
        limit=limit,
        offset=offset,
    )


@router.get(
    '/{user_id}',
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name='get_user',
)
async def get_user(
    user_id: int,
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> UserRead:
    try:
        result = await repository.get(model_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID={user_id} not found'
        )
    return result


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    name='delete_user',
)
async def delete_user(
    user_id: int,
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> None:
    try:
        await repository.get(model_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Article with ID={user_id} not found'
        )
    return await repository.delete(model=User, model_id=user_id)


@router.post(
    '/{user_id}/districts',
    response_model=DistrictRead,
    status_code=status.HTTP_201_CREATED,
    name='create_user_district',
)
async def create_user_district(
    user_id: int,
    district_create: DistrictCreate = Body(...),
    repository: DistrictRepository = Depends(get_repository(DistrictRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> DistrictRead:
    try:
        return await repository.create(
            model_id=user_id, district_create=district_create, parent_model=User
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Customer with ID={user_id} not found'
        )


@router.post(
    '/{user_id}/districts/{district_id}',
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    name='delete_user_district',
)
async def delete_user_district(
    user_id: int,
    district_id: int,
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> UserRead:
    try:
        return await repository.delete_district(
            district_id=district_id, model_id=user_id
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User or district not found'
        )


@router.get(
    '/{user_id}/articles',
    response_model=ArticleRead,
    status_code=status.HTTP_200_OK,
    name='get_user_articles',
)
async def get_user_articles(
    user_id: int,
    repository: UserRepository = Depends(get_repository(UserRepository)),
    api_key: APIKey = Depends(get_api_key),
) -> list[Optional[ArticleRead]]:
    try:
        return await repository.list_articles(model_id=user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found'
        )
