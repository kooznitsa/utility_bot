import os

from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class Settings(BaseConfig):
    bot_token: str = os.environ.get('BOT_TOKEN')
    redis_url: str = os.environ.get('REDIS_URL')

    class Config:
        env_file = '.env'


settings = Settings()
