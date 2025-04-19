import streamlit as st
import pickle
import pandas as pd
import requests

def load_similarity():
    url = "https://huggingface.co/SonaliB15/movie-recommender-data/blob/main/similarity.pkl"
    response = requests.get(url)
    return pickle.load(response.content)

# Load movie data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = load_similarity()

# Extract movie titles for dropdown
movie_titles = movies_df['title'].tolist()  # Keep this as a list for Streamlit selectbox

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d262e0c6f160ea9a84206c3625ac8ad6&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    if movie not in movie_titles:
        return ["Movie not found!"]
    
    movie_index = movies_df[movies_df['title'] == movie].index[0]  # Get the index of the movie
    distances = similarity[movie_index]  # Get similarity scores
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []  
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]]['movie_id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Search a movie:', movie_titles)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
