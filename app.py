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

# ---------------------------
# RECOMMEND FUNCTION
# ---------------------------
def recommend(movie):
    recommended_movies = []

    movie_index = data[data['title'] == movie].index[0]
    distance = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distance)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    for i in movie_list:
        recommended_movies.append(data.iloc[i[0]].title)

    return recommended_movies

# UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

/* Title */
.title {
    text-align: center;
    font-size: 80px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: white;
}

/* Movie List Item */
.movie-item {
    background: rgba(255,255,255,0.15);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 18px;
    color: white;
    font-weight: 500;
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
        movies = recommend(selected_movie)

    st.write("")
    st.subheader("Recommended Movies")

    # ✅ CORRECT INDENTATION HERE
    for movie in movies:
        st.markdown(f"""
        <div class="movie-item">
            🎬 {movie}
        </div>
        """, unsafe_allow_html=True)
