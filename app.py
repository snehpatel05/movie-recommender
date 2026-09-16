import os
import pickle

import requests
import streamlit as st


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
if not TMDB_API_KEY:
    try:
        TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", "")
    except Exception:
        TMDB_API_KEY = ""


@st.cache_data
def load_data():
    with open("movies.pkl", "rb") as movies_file:
        movie_data = pickle.load(movies_file)
    with open("similarity.pkl", "rb") as similarity_file:
        similarity_data = pickle.load(similarity_file)
    return movie_data, similarity_data


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    poster_path = response.json().get("poster_path")
    return f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None


def recommend(movie, movie_data, similarity_data):
    movie_index = movie_data[movie_data["title"] == movie].index[0]
    distances = similarity_data[movie_index]
    movie_indices = sorted(
        enumerate(distances), reverse=True, key=lambda item: item[1]
    )[1:6]

    names = []
    posters = []
    for index, _ in movie_indices:
        names.append(movie_data.iloc[index].title)
        posters.append(fetch_poster(movie_data.iloc[index].id))
    return names, posters


st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
st.title("🎬 Movie Recommender System")
st.write("Choose a movie you like and discover five similar movies.")

movies, similarity = load_data()
selected_movie = st.selectbox("Select a movie", movies["title"].tolist())

if st.button("Recommend", type="primary"):
    if not TMDB_API_KEY:
        st.error("TMDB_API_KEY is missing. Add it to Render environment variables.")
    else:
        try:
            names, posters = recommend(selected_movie, movies, similarity)
            columns = st.columns(5)
            for column, name, poster in zip(columns, names, posters):
                with column:
                    st.subheader(name)
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.info("Poster unavailable")
        except requests.RequestException:
            st.error("TMDB is temporarily unavailable. Please try again.")
    