import pickle
import streamlit as st
import requests


API_KEY = "10480544922acc8365d63980616509a2"  


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
       
        response = requests.get(url, timeout=8)
        response.raise_for_status()            
        data = response.json()
    except requests.exceptions.RequestException as e:

        print("TMDB request error:", e)
        
        return "https://placehold.co/400x600?text=No+Poster"

    poster_path = data.get("poster_path")
    if not poster_path:
        return "https://placehold.co/400x600?text=No+Poster"

   
    return "https://image.tmdb.org/t/p/w500" + poster_path



movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i, score in distances[1:50]:
        movie_id = movies.iloc[i]['movie_id']
        title = movies.iloc[i]['title']

        poster_url = fetch_poster(movie_id)
        if "No+Poster" in poster_url:
            continue

        recommended_movie_names.append(title)
        recommended_movie_posters.append(poster_url)

        if len(recommended_movie_names) == 5:
            break

    return recommended_movie_names, recommended_movie_posters



# 🎬 Streamlit UI
st.header('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])