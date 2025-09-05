import pickle
import pandas as pd
import streamlit as st
import requests

#Load data
movies = pickle.load(open('movie_dict.pkl', 'rb'))
data = pd.DataFrame(movies)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#TMDB API key
API_KEY = "0361c880dff8292ad595e26765c54f45"

def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass

    #fallback poster (same size as others)
    return "https://via.placeholder.com/300x450/222222/FFFFFF?text=No+Poster"


def recommend(movie):
    movie_index = data[data['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        title = data.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))
    return recommended_movies, recommended_posters

# Web app
st.title("🍿 Movie Recommendation System 🎬")
st.markdown("Find movies similar to your favorite one!")

selected_movie = st.selectbox("🎥 Select a movie", list(data['title'].values))
btn = st.button("🔍 Recommend")

if btn:
    names, posters = recommend(selected_movie)

    # Display in grid
    cols = st.columns(4)
    for i in range(len(names)):
        with cols[i % 4]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f"**{names[i]}**", unsafe_allow_html=True)
