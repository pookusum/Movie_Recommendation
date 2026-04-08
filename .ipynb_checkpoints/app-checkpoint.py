import pickle 
import pandas as pd
import streamlit as st 

# load the data

data = pickle.load(open('movie_dict.pkl', mode='rb'))
data = pd.DataFrame(data)
#print(movies) 


similarity = pickle.load(open('similarity.pkl', mode='rb'))
print(similarity)

#Final function
def recommend(movie):


    recommended_movies = []

    movie_index = data[data['title']== movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse= True, key= lambda x: x[1])[1:6]

    for i in movie_list:
      #  print(i[0])
      print(data.iloc[i[0]].title)

    return recommended_movies      


#streamlit web app

st.title('Movie Recommendation System')

import streamlit as st

Selected_Movie = st.selectbox("Select a movie to get a recommendation", data['title'].values)
btn=st.button('Recommend')

if btn:
   
    list_of_movies= recommend(Selected_Movie)
     
    for movie in list_of_movies:
      st.write(movie)

