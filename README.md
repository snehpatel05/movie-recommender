# Reelwise

### Find your next great watch.

Reelwise is a content-based movie recommendation app built with Streamlit. Choose a movie you already enjoy and get five similar films, complete with live TMDB poster artwork.

The app combines a precomputed cosine-similarity model with a clean, cinema-inspired interface designed for quick discovery.

## Features

- Browse a library of 4,800+ movies.
- Get five recommendations from a movie you select.
- Use a precomputed content-based similarity model for fast results.
- Fetch current poster artwork from TMDB.
- Responsive Streamlit layout with a dark cinema theme.
- Deploy directly to Streamlit Community Cloud.

## How It Works

The recommendation engine uses two saved model artifacts:

- `movies.pkl` contains the movie dataset and titles.
- `similarity.pkl` contains the precomputed similarity matrix.

When a movie is selected, the app finds its row in the dataset, ranks the closest movies by similarity score, and requests each poster from TMDB.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/snehpatel05/movie-recommender.git
cd movie-recommender
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your TMDB key

Create `.streamlit/secrets.toml`:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

Never commit this file or place the key directly in `app.py`.

### 4. Start the app

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Deploy On Streamlit Community Cloud

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app**.
3. Select `snehpatel05/movie-recommender`.
4. Choose the `main` branch.
5. Set the main file to `app.py`.
6. Open **Advanced settings**.
7. Add this secret using your own TMDB key:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

8. Click **Deploy**.

Streamlit will build the app and provide a public `.streamlit.app` URL.

## Project Structure

```text
movie-recommender/
├── app.py                         # Streamlit interface and recommendation logic
├── movies.pkl                     # Movie dataset
├── similarity.pkl                 # Precomputed similarity matrix
├── requirements.txt               # Python dependencies
└── .gitignore                     # Local files and secrets excluded from Git
```

## Tech Stack

- Python
- Streamlit
- Pandas
- Requests
- Pickle
- TMDB API

## Important Notes

- The TMDB key belongs in Streamlit Secrets only.
- `movies.pkl` and `similarity.pkl` must stay in the repository root.
- Poster artwork depends on TMDB availability and a valid API key.
- The recommendation model does not require retraining to run the app.

## Credits

Movie metadata and poster artwork are provided by [The Movie Database (TMDB)](https://www.themoviedb.org/).

Built by [Sneh Patel](https://github.com/snehpatel05).
