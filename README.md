# Movie Recommender

A simple Streamlit movie recommender using the original content-based model and TMDB posters.

## Local setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud

1. Open [share.streamlit.io](https://share.streamlit.io/).
2. Choose this GitHub repository and the `main` branch.
3. Set the main file to `app.py`.
4. Add this secret in **Advanced settings**:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

The model artifacts `movies.pkl` and `similarity.pkl` must remain in the project root.
