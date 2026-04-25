import pickle
import pandas as pd
import streamlit as st
import os
import requests


st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: white;
}
.title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #E50914;
}
.subtext {
    text-align: center;
    font-size: 18px;
    color: #bbbbbb;
}
.movie-card {
    background-color: #1c1c1c;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Download files
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
# Load data
# ---------------------------
data = pickle.load(open("movie_dict.pkl", "rb"))
data = pd.DataFrame(data)

similarity = pickle.load(open("similarity.pkl", "rb"))

# ---------------------------
# Recommendation function
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


# ---------------------------
# Streamlit UI (UPDATED)
# ---------------------------

# Title Section
st.markdown('<p class="title">🎬 Movie Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Discover movies similar to your favorites</p>', unsafe_allow_html=True)

# Spacer
st.write("")

# Movie Selection
selected_movie = st.selectbox(
    "🎥 Choose a movie",
    data['title'].values
)

# Button
if st.button("🚀 Recommend"):
    
    with st.spinner("Finding best movies for you... 🍿"):
        list_of_movies = recommend(selected_movie)

    st.write("")
    st.subheader("✨ Recommended Movies")

    # Display in Grid (NEW)
    cols = st.columns(5)

    for i in range(len(list_of_movies)):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card">
                <h4>{list_of_movies[i]}</h4>
            </div>
            """, unsafe_allow_html=True)
