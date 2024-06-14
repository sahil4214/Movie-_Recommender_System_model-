import pickle
import streamlit as st
import requests

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        return data
    except requests.exceptions.RequestException as e:
        st.error("Failed to fetch movie details.")
        return None

def fetch_poster(movie_id):
    details = fetch_movie_details(movie_id)
    if details and 'poster_path' in details:
        poster_path = details['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    return "https://via.placeholder.com/500"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_ids = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_ids.append(movie_id)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_ids

def display_movie_info(movie_id):
    details = fetch_movie_details(movie_id)
    if details:
        st.image(fetch_poster(movie_id))
        st.write(f"**Title:** {details.get('title', 'N/A')}")
        st.write(f"**Overview:** {details.get('overview', 'N/A')}")
        st.write(f"**Release Date:** {details.get('release_date', 'N/A')}")
        st.write(f"**Rating:** {details.get('vote_average', 'N/A')}")

st.header('Movie Recommender System')

# Load movie data and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Dropdown menu for selecting a movie
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)

    st.write(f"### Selected Movie: {selected_movie}")
    selected_movie_id = movies[movies['title'] == selected_movie].iloc[0].movie_id
    display_movie_info(selected_movie_id)

    st.write("### Recommended Movies:")
    cols = st.columns(5)
    for col, name, poster, movie_id in zip(cols, recommended_movie_names, recommended_movie_posters, recommended_movie_ids):
        with col:
            if st.button(name):
                display_movie_info(movie_id)
            st.image(poster)
