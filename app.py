import os
import pickle
import requests
from pathlib import Path
import streamlit as st

# Function to download file from Google Drive
import gdown
import os

def download_similarity():
    if not os.path.exists("similarity.pkl"):
        url = "https://drive.google.com/uc?id=1VSLh4SjTTvNA7pl6m0gAKJTDeqnZ3JQW"
        gdown.download(url, "similarity.pkl", quiet=False)
        print("similarity.pkl downloaded!")
    else:
        print("similarity.pkl already exists!")

download_similarity()


# Download similarity.pkl dynamically
SIMILARITY_FILE_ID = "1VSLh4SjTTvNA7pl6m0gAKJTDeqnZ3JQW"
download_file(SIMILARITY_FILE_ID, "similarity.pkl")

# Ensure movie_list.pkl exists in repo
MOVIE_LIST_FILE = "movie_list.pkl"
if not os.path.exists(MOVIE_LIST_FILE):
    st.error("movie_list.pkl not found! Upload it to the repo.")
    st.stop()

# Load files
with open(MOVIE_LIST_FILE, "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Movie selection
movie_list = movies["title"].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Recommendation logic
def fetch_poster(movie_id):
    api_key = "1e16d0940d1b72934b095fd257a59866"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

if st.button("Show Recommendation"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])









