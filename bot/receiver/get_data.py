import json
import urllib.request

from config_data.config import settings


def get_data(user_id: int):
    url = f'{settings.gw_root_url}/users/{user_id}/articles'
    # TODO: send API key

    with urllib.request.urlopen(url) as url:
        data = json.load(url)

    return data
