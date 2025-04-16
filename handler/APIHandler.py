import requests
from fastapi import HTTPException
import numpy
import pandas

class APIHandler:

    @staticmethod
    def fetch_info(movie_id):
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7a73cdf477499a24ab38bdbb2f809f9e'
        )
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        data = response.json()
        return {
            "poster": f'https://image.tmdb.org/t/p/w154/{data.get("poster_path", "")}',
            "desc": data.get("overview", "No description available"),
            "rating": data.get("vote_average", "No rating available")
        }
    
    @staticmethod
    def recommend(movies:pandas.core.frame.DataFrame, similarity:numpy.ndarray, movie: str):
        if movie not in movies['title'].values:
            raise HTTPException(status_code=404, detail="Movie not found in dataset")
        
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movie_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[:9]  # Top 9 similar movies
        
        recommendations = {
            "movies_name": [],
            "movies_poster": [],
            "movies_description": [],
            "movies_rating": []
        }
        
        for i in movie_list:
            movie_title = movies.iloc[i[0]].title
            info = APIHandler.fetch_info(movies.iloc[i[0]].movie_id)
            
            recommendations["movies_name"].append(movie_title)
            recommendations["movies_poster"].append(info["poster"])
            recommendations["movies_description"].append(info["desc"])
            recommendations["movies_rating"].append(info["rating"])
        
        return recommendations