import streamlit as st
import pickle
import pandas as pd
import requests


movies_dict = pickle.load(open('models/movies_dict.pkl', 'rb'))
similarity = pickle.load(open('models/similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie-Recommender-System")

selected_movie_name = st.selectbox("Select your  favourite movie, and we will recommend you your next movie ",
                                   movies['title'].values)
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f1ab5488ecf1d785c1b78e2a5b328bda&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies=[]
    recommend_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fetch poster from api
        recommend_movies_poster.append(fetch_poster(movie_id))

        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_poster



if st.button("Recommend-movie"):
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
