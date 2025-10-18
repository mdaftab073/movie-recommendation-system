import os
import pickle
from pathlib import Path

import streamlit as st
import requests
import time


def fetch_poster(movie_id):
    """Fetch poster URL using TMDB API key from environment variable TMDB_API_KEY.

    Falls back to a placeholder image if the key is missing or the request fails.
    """
    api_key = "1e16d0940d1b72934b095fd257a59866"
    if not api_key:
        # don't raise here; allow the app to run but warn the user in the UI
        st.warning("TMDB_API_KEY not set. Poster images may not load.")

    if api_key:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    else:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"

    for attempt in range(3):  # try up to 3 times
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                return "https://via.placeholder.com/500x750?text=No+Poster"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching poster (attempt {attempt+1}/3): {e}")
            time.sleep(2)
    return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header("Movie Recommender System")

# Resolve data files relative to this script so deployments work without absolute paths
base = Path(__file__).parent
movie_list_path = base / "movie_list.pkl"
similarity_path = base / "similarity.pkl"

# Try relative path first, then fallback to the old absolute path for compatibility
if movie_list_path.exists() and similarity_path.exists():
    movies = pickle.load(open(movie_list_path, "rb"))
    similarity = pickle.load(open(similarity_path, "rb"))
else:
    alt_movie_list = Path("D:/machine learning/projects/movies recommendation/movie_list.pkl")
    alt_similarity = Path("D:/machine learning/projects/movies recommendation/similarity.pkl")
    if alt_movie_list.exists() and alt_similarity.exists():
        movies = pickle.load(open(alt_movie_list, "rb"))
        similarity = pickle.load(open(alt_similarity, "rb"))
    else:
        st.error("Required data files movie_list.pkl and similarity.pkl not found.\nPlace them next to app.py or set correct paths.")
        st.stop()


movie_list = movies["title"].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])






