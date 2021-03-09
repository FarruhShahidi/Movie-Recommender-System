import numpy as np
from tmdbv3api import TMDb
import json
import requests


tmdb = TMDb()
tmdb.api_key = '2239848dd3e0d8e43cf2add39e687057'

from tmdbv3api import Movie
tmdb_movie = Movie()
def get_genre(movie):
    genres = []
    result = tmdb_movie.search(movie)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    if data_json['genres']:
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
        return str(genres)

    return np.NaN
