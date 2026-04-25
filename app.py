import pickle
import pandas as pd
import streamlit as st
import os
import requests

# ---------------------------
# DOWNLOAD FILES 
# ---------------------------
def download_file(url, filename):
    if not os.path.exists(filename):
        with requests.get(url, stream=True) as r:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

MOVIE_DICT_URL = "https://huggingface.co/datasets/PoojaKusum/movie-recommendation-files/resolve/main/movie_dict.pkl"
SIMILARITY_URL = "https://huggingface.co/datasets/PoojaKusum/movie-recommendation-files/resolve/main/similarity.pkl"

download_file(MOVIE_DICT_URL, "movie_dict.pkl")
download_file(SIMILARITY_URL, "similarity.pkl")

# ---------------------------
# LOAD DATA
# ---------------------------
data = pickle.load(open("movie_dict.pkl", "rb"))
data = pd.DataFrame(data)

similarity = pickle.load(open("similarity.pkl", "rb"))


def fetch_poster(movie_name):
    try:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey=http://www.omdbapi.com/?i=tt3896198&apikey=a5784b03"
        data_api = requests.get(url, timeout=5).json()

        if data_api.get('Response') == 'True':
            poster = data_api.get('Poster')
            if poster and poster != "N/A":
                return poster

        return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

# ---------------------------
# RECOMMEND FUNCTION
# ---------------------------
def recommend(movie):
    recommended_movies = []
    recommended_posters = []

    movie_index = data[data['title'] == movie].index[0]
    distance = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distance)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movie_list:
        title = data.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters
# ---------------------------
# UI DESIGN
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Title */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #dcdcdc;
}

/* Card */
.movie-card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    padding: 10px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown('<p class="title">🎬 Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover movies you’ll love 🍿</p>', unsafe_allow_html=True)

st.write("")

# ---------------------------
# INPUT
# ---------------------------
selected_movie = st.selectbox(
    "🎥 Choose a movie",
    data['title'].values
)

# ---------------------------
# BUTTON
# ---------------------------
if st.button("🚀 Get Recommendations"):

    with st.spinner("Finding best movies for you... 🍿"):
        movies, posters = recommend(selected_movie)

    st.write("")
    st.subheader("✨ Recommended Movies")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"<p style='text-align:center'>{movies[i]}</p>", unsafe_allow_html=True)
