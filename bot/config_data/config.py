import os

from dotenv import load_dotenv
from pydantic import BaseConfig

load_dotenv()


class Settings(BaseConfig):
    bot_token: str = os.environ.get('BOT_TOKEN')

    class Config:
        env_file = '.env'


settings = Settings()
