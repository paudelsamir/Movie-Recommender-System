import streamlit as st
import pickle
import requests
import time

movies = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies['title'].tolist()
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

option = st.selectbox('Select the movie 📽️', movies_list)

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1940039a2065b5f00f0416cf17fe5238&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

if st.button('Recommend'):
    with st.spinner('Fetching ...'):
        time.sleep(0.1)
        names, posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    for idx, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{posters[idx]}" style="width: 100%; border-radius: 10px; transition: 0.3s; cursor: pointer;" 
                    onmouseover="this.style.transform='scale(1.1)'" 
                    onmouseout="this.style.transform='scale(1)'" />
                    <p style="margin-top: 5px;">{names[idx]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
