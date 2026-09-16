# Reelwise

A lightweight movie recommender with the original content-based model, a Flask API, and a single HTML/CSS/JavaScript frontend.

## Local setup

```bash
pip install -r requirements.txt
$env:TMDB_API_KEY="your_tmdb_api_key"
python app.py
```

Open `http://localhost:5000`.

## Render deployment

Create a new **Web Service** from this repository. Render can use the included `render.yaml`, or set:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --timeout 120 --bind 0.0.0.0:$PORT app:app`
- Environment variable: `TMDB_API_KEY` with your TMDB v3 API key

The model artifacts `movies.pkl` and `similarity.pkl` must remain in the project root.
