


# movies/services.py
import requests

API_KEY = "3ad5c20e"
BASE_URL = "http://www.omdbapi.com/"


def search_movies_api(query):
    params = {"apikey": API_KEY, "s": query}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data.get("Search", [])
    return []


def get_movie_detail_api(imdb_id):
    params = {"apikey": API_KEY, "i": imdb_id, "plot": "full"}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "True":
        return data
    return None
