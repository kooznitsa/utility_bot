import json
import urllib.request

from config_data.config import settings


def get_data(user_id: int):
    url = f'{settings.redis_url}/api/users/{user_id}/articles'

    with urllib.request.urlopen(url) as url:
        data = json.load(url)

    return data
