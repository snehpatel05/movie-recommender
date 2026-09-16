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


st.set_page_config(page_title="Reelwise", page_icon="🎞️", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp {
        background: radial-gradient(circle at 10% 0%, #25233a 0, #101116 34%, #090a0e 75%);
        color: #f6f3ee;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { visibility: hidden; }
    .block-container { max-width: 1180px; padding: 3rem 3rem 5rem; }
    h1, h2, h3, p, label, .stMarkdown { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; }
    .brand { color: #ffc857; font-size: .75rem; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; }
    .hero-title { margin: .8rem 0 .8rem; font-family: 'Space Grotesk', sans-serif; font-size: clamp(2.8rem, 7vw, 5.9rem); font-weight: 700; letter-spacing: -.07em; line-height: .94; }
    .hero-title span { color: #ff7043; }
    .hero-copy { max-width: 570px; color: #a7aab4; font-size: 1.05rem; line-height: 1.6; }
    .search-label { margin-top: 2.5rem; color: #a7aab4; font-size: .78rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
    div[data-baseweb="select"] > div { min-height: 52px; border: 1px solid rgba(255,255,255,.14); border-radius: 12px; background: rgba(255,255,255,.08); }
    div[data-baseweb="select"] > div:hover { border-color: #ffc857; }
    .stButton > button { min-height: 50px; margin-top: 1.8rem; border: 0; border-radius: 12px; color: #111116; background: #ffc857; font-weight: 700; transition: transform .2s, background .2s; }
    .stButton > button:hover { color: #111116; background: #ffd979; transform: translateY(-2px); }
    .section-title { margin: 4rem 0 1.4rem; font-family: 'Space Grotesk', sans-serif; font-size: 1.7rem; font-weight: 700; letter-spacing: -.04em; }
    .section-title span { color: #7d8290; font-size: .85rem; font-family: 'DM Sans', sans-serif; font-weight: 400; letter-spacing: 0; }
    .movie-name { min-height: 3.2rem; margin: .9rem 0 .3rem; color: #f6f3ee; font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600; line-height: 1.25; }
    .movie-rank { color: #ff7043; font-size: .72rem; font-weight: 700; letter-spacing: .15em; }
    [data-testid="stImage"] img { border-radius: 12px; border: 1px solid rgba(255,255,255,.1); box-shadow: 0 18px 35px rgba(0,0,0,.28); }
    .hint { margin-top: 4rem; color: #626775; font-size: .78rem; }
    </style>
    <div class="brand">Reelwise · personalized cinema</div>
    <div class="hero-title">Find your next<br><span>great watch.</span></div>
    <div class="hero-copy">Pick a movie you already love. Discover five films with the same energy, story, and atmosphere.</div>
    """,
    unsafe_allow_html=True,
)

movies, similarity = load_data()
st.markdown('<div class="search-label">Start with a movie</div>', unsafe_allow_html=True)
selected_movie = st.selectbox(
    "Start with a movie",
    movies["title"].tolist(),
    label_visibility="collapsed",
)

if st.button("Discover recommendations  →", type="primary", use_container_width=True):
    if not TMDB_API_KEY:
        st.error("TMDB_API_KEY is missing. Add it to Streamlit Secrets.")
    else:
        try:
            names, posters = recommend(selected_movie, movies, similarity)
            st.markdown(
                f'<div class="section-title">Because you liked {selected_movie} <span>· five picks for your watchlist</span></div>',
                unsafe_allow_html=True,
            )
            columns = st.columns(5)
            for index, (column, name, poster) in enumerate(zip(columns, names, posters), 1):
                with column:
                    st.markdown(f'<div class="movie-rank">0{index} / RECOMMENDED</div>', unsafe_allow_html=True)
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.markdown('<div class="poster-missing">Poster unavailable</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="movie-name">{name}</div>', unsafe_allow_html=True)
        except requests.RequestException:
            st.error("TMDB is temporarily unavailable. Please try again.")

st.markdown('<div class="hint">Powered by your taste and a content-based recommendation model.</div>', unsafe_allow_html=True)
    