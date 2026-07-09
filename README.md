# 🎬 Movie Recommender

A content-based movie recommendation web app built with Python and Streamlit. Pick a movie you like, and it suggests 5 similar movies along with their posters, fetched live from The Movie Database (TMDB).

[![Live App](https://img.shields.io/badge/🚀%20Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://movie-recommender-by-sneh.streamlit.app/)  Made by [Sneh Patel](https://github.com/snehpatel05)

## How it works

The app uses a precomputed cosine-similarity matrix (`similarity.pkl`) built over a movie dataset (`movies.pkl`). When you select a movie:

1. It looks up that movie's index in the dataset.
2. It finds the 5 most similar movies based on similarity scores.
3. It calls the TMDB API to fetch each recommended movie's poster.
4. It displays the recommended titles and posters side by side.

## Tech stack

- **Python**
- **Streamlit** – web app framework / UI
- **Pandas** – data handling
- **Requests** – calling the TMDB API
- **Pickle** – loading the precomputed movie dataset and similarity matrix
- **TMDB API** – fetching movie posters

## Project structure

```
movie-recommender/
├── app.py              # Streamlit app (UI + recommendation logic)
├── movies.pkl           # Preprocessed movie dataset
├── similarity.pkl        # Precomputed cosine similarity matrix
└── requirements.txt       # Python dependencies
```

## Running it locally

1. **Clone the repo**
   ```bash
   git clone https://github.com/snehpatel05/movie-recommender.git
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your TMDB API key**

   The app reads the key from Streamlit secrets. Create a file at `.streamlit/secrets.toml` in the project root:
   ```toml
   TMDB_API_KEY = "your_tmdb_api_key_here"
   ```
   You can get a free API key by creating an account at [themoviedb.org](https://www.themoviedb.org/) and generating one in your account settings.

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. Open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## Usage

- Select a movie from the dropdown.
- Click **Recommend**.
- Browse the 5 recommended movies with their posters.

## Deployment

This app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud). If you fork this repo and deploy your own copy, remember to add your `TMDB_API_KEY` under your app's **Settings → Secrets** on Streamlit Cloud instead of a local `secrets.toml` file.

## License

This project currently has no license specified. Feel free to reach out to the repo owner if you'd like to use it beyond personal/learning purposes.
