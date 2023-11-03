from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from database.config import settings

API_KEY_HEADER = APIKeyHeader(name='X-API-Key')


async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == settings.gw_api_key:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='API Key is invalid or missing',
        )
