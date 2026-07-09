import streamlit as st
import pickle
import requests 

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}".format(movie_id, api_key))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommended_movies=[]
    recommend_movies_posters=[]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommend_movies_posters

st.title("Movie Recommender System")
movies=pickle.load(open("movies.pkl","rb"))
similarity=pickle.load(open("similarity.pkl","rb"))
movies_li=movies['title'].values
selected_movie_name=st.selectbox("Enter a movie",movies_li)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    columns = st.columns(5)
    
    for index, col in enumerate(columns):
        with col:
            st.markdown(
                f"<div style='height: 90px; font-size: 14px; font-weight: 600; line-height: 1.3;'>{names[index]}</div>", 
                unsafe_allow_html=True
            )
            st.image(posters[index])
