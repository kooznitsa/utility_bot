import httpx
import logging
from typing import Optional, Union
from json import JSONDecodeError

from .logger import gateway_api_driver_logger_init
from config_data.config import settings
from schemas.schemas import UserCreate, DistrictCreate


class GatewayAPIDriver:
    _api_root_url: str = settings.gw_root_url
    _headers = {'X-API-Key': settings.gw_api_key}

    logger: logging.Logger = gateway_api_driver_logger_init()

    class LoggerMsgTemplates:
        REQUEST: str = 'REQUEST: url: {url} headers: {headers} body: {body}'
        RESPONSE: str = (
            'RESPONSE: status_code: {status_code} url: {url} headers: {headers} '
            'body: {body} error: {error}'
        )

    class Route:
        users: str = '/users'

        @staticmethod
        def get_districts_url(user_id: int):
            return f'/users/{user_id}/districts'

    @classmethod
    async def _build_url(cls, route: str) -> str:
        return f'{cls._api_root_url}{route}'

    @classmethod
    async def _post_data(cls, url: str, data) -> httpx.Response:
        cls._log_request(url, cls._headers, data)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                headers=cls._headers,
                data=data,
            )

        try:
            resp_body = resp.json()
            error = None
        except JSONDecodeError as exc:
            resp_body = None
            error = str(exc)

        cls._log_response(resp.url, resp.status_code, resp.headers, resp_body, error)

        return resp

    @classmethod
    async def tg_user_create(cls, user_create: UserCreate) -> httpx.Response:
        url = await cls._build_url(cls.Route.users)
        return await cls._post_data(url, user_create)

    @classmethod
    async def tg_district_create(cls, user_id: int, district_create: DistrictCreate) -> httpx.Response:
        url = await cls._build_url(cls.Route.get_districts_url(user_id))
        return await cls._post_data(url, district_create)

    @classmethod
    def _log_request(cls, url: str, headers: dict[str, str], body: dict) -> None:
        cls.logger.info(
            msg=cls.LoggerMsgTemplates.REQUEST.format(
                url=url,
                headers=headers,
                body=body,
            )
        )

    @classmethod
    def _log_response(
            cls,
            url: Optional[httpx.URL],
            status_code: int,
            headers: dict[str, str],
            body: Union[None, dict, str] = None,
            error: Optional[str] = None,
    ) -> None:
        cls.logger.info(
            msg=cls.LoggerMsgTemplates.RESPONSE.format(
                url=url,
                status_code=status_code,
                headers=headers,
                body=body,
                error=error,
            )
        )
