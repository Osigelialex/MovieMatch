from models import userProfile
import requests
import os


def get_movie_by_params(genre, language):
    api_key = os.getenv('API_KEY2')
    params = {
        "api_key": api_key,
        "with_original_language": language,
        "with_genres": genre,
        # "sort_by": 'vote_average.desc'
        "page": 1
    }
    base_url = 'https://api.themoviedb.org/3/discover/movie'
    response = requests.get(base_url, params=params)
    data = response.json()
    return data


def get_trending_movies(api_key):
    url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results']