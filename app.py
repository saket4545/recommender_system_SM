import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0e90bdd1621f41f1093207aeaf9ac4b8')
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get('poster_path')
        vote_average = data.get('vote_average',)
        if poster_path:
            return f'https://image.tmdb.org/t/p/w500/{poster_path}'
        else:
            return 'https://via.placeholder.com/500'
    else:
        st.error(f"Failed to fetch poster for movie ID {movie_id}. Status code: {response.status_code}")
        return 'https://via.placeholder.com/500'

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distance = similarity[movie_index]
        movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
        L = []
        P = []
        v =[]
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            L.append(movies.iloc[i[0]].title)
            P.append(fetch_poster(movie_id))
        return L, P
    except Exception as e:
        st.error(f"An error occurred in the recommendation function: {e}")
        return [], []



st.header('Movie Recommender System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection
selected_movie = st.selectbox(
    "Select the Movie name", movies['title'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie)

    if not posters or not recommendations:
        st.error("No recommendations or posters available.")
    else:
        cols = st.columns(5)
        for col, rec, poster in zip(cols, recommendations, posters):
            with col:
                st.text(rec)
                st.image(poster, use_column_width=True)