import os
import pickle
from functools import lru_cache

import requests
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p"
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")

with open("movies.pkl", "rb") as movies_file:
    movies = pickle.load(movies_file)
with open("similarity.pkl", "rb") as similarity_file:
    similarity = pickle.load(similarity_file)


def image_url(path, size="w500"):
    return f"{TMDB_IMAGE_URL}/{size}{path}" if path else None


@lru_cache(maxsize=256)
def fetch_movie_details(movie_id):
    if not TMDB_API_KEY:
        raise RuntimeError("TMDB_API_KEY is not configured")

    response = requests.get(
        f"{TMDB_BASE_URL}/movie/{movie_id}",
        params={
            "api_key": TMDB_API_KEY,
            "language": "en-US",
            "append_to_response": "credits",
        },
        timeout=8,
    )
    response.raise_for_status()
    data = response.json()
    data["poster_url"] = image_url(data.get("poster_path"))
    data["backdrop_url"] = image_url(data.get("backdrop_path"), "original")
    data["cast"] = [person["name"] for person in data.get("credits", {}).get("cast", [])[:3]]
    data.pop("credits", None)
    return data


def recommendation_rows(title):
    matches = movies[movies["title"] == title]
    if matches.empty:
        return None

    movie_index = matches.index[0]
    distances = similarity[movie_index]
    recommended_indices = sorted(
        enumerate(distances), reverse=True, key=lambda item: item[1]
    )[1:6]

    recommendations = []
    for index, score in recommended_indices:
        movie_id = int(movies.iloc[index].id)
        details = fetch_movie_details(movie_id)
        details["similarity"] = round(float(score), 4)
        recommendations.append(details)
    return recommendations


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/movies")
def movie_titles():
    return jsonify({"movies": movies["title"].tolist()})


@app.post("/api/recommend")
def recommend():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "").strip()
    if not title:
        return jsonify({"error": "Choose a movie first."}), 400

    try:
        recommendations = recommendation_rows(title)
    except RuntimeError as error:
        return jsonify({"error": str(error)}), 500
    except requests.RequestException:
        return jsonify({"error": "TMDB is temporarily unavailable. Try again shortly."}), 502

    if recommendations is None:
        return jsonify({"error": "That movie is not in the recommendation dataset."}), 404
    return jsonify({"selected": title, "recommendations": recommendations})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    