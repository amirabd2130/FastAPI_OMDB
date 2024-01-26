import os

import requests
from include import exceptions

URL = "https://www.omdbapi.com/"

FASTAPI_OMDB_OMDB_API_URL = os.environ.get("FASTAPI_OMDB_OMDB_API_URL")
FASTAPI_OMDB_OMDB_API_KEY = os.environ.get("FASTAPI_OMDB_OMDB_API_KEY")
if not FASTAPI_OMDB_OMDB_API_URL or not FASTAPI_OMDB_OMDB_API_KEY:
    raise exceptions.INTERNAL_SERVER_ERROR


def get_movie_detail_by_title(titleString, page=1, searchType="s"):
    params = {
        "apikey": FASTAPI_OMDB_OMDB_API_KEY,
        "type": "movie",
        searchType: titleString,
        "page": page,
        "r": "json",
    }
    response = requests.get(FASTAPI_OMDB_OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            if searchType == "s":
                return data.get("Search", [])
            else:
                return data
        else:
            raise exceptions.OMDB_API_ERROR
    return None


def get_movie_detail_by_id(imdb_id):
    params = {
        "apikey": FASTAPI_OMDB_OMDB_API_KEY,
        "i": imdb_id,
        "r": "json",
    }

    response = requests.get(FASTAPI_OMDB_OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data

    return True
