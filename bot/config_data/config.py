import logging
import os

from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class Settings(BaseConfig):
    redis_url: str = os.environ.get('REDIS_URL')

    bot_token: str = os.environ.get('BOT_TOKEN')
    tg_api_id: str = os.environ.get('TG_API_ID')
    tg_api_hash: str = os.environ.get('TG_API_HASH')
    tg_session_name: str = os.environ.get('TG_SESSION_NAME')

    gw_root_url: str = os.environ.get('GW_ROOT_URL')
    gw_api_key: str = os.environ.get('GW_API_KEY')

    logs_dir: str = 'logs/'

    class GatewayAPIDriverLogger:
        filename: str = 'gateway_api_driver.log'
        max_bytes: int = 5 * (1024 * 1024)
        backup_count: int = 10
        formatter: logging.Formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    class Config:
        env_file = '.env'


settings = Settings()
