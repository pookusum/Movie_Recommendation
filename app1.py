import pickle
import pandas as pd
import streamlit as st
import os
import gdown

# ---------------------------
# Download PKL files only if missing
# ---------------------------
MOVIE_DICT_URL = "https://drive.google.com/uc?id=YOUR_MOVIE_DICT_FILE_ID"
SIMILARITY_URL = "https://drive.google.com/uc?id=YOUR_SIMILARITY_FILE_ID"

if not os.path.exists("movie_dict.pkl"):
    gdown.download(MOVIE_DICT_URL, "movie_dict.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download(SIMILARITY_URL, "similarity.pkl", quiet=False)

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
# Streamlit UI
# ---------------------------
st.title("Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie to get a recommendation",
    data['title'].values
)

if st.button("Recommend"):
    list_of_movies = recommend(selected_movie)

    st.subheader("Recommended Movies:")
    for movie in list_of_movies:
        st.success(movie)