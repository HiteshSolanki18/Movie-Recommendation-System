import streamlit as st
import pickle
import requests
import pandas as pd

st.title('Movie Recommedar System', anchor=None)

df = pickle.load(open('movies_titles.pkl','rb'))

similarity_distance = pickle.load(open('similarity.pkl','rb'))

final_df = pd.DataFrame(df)

movie_list = final_df['title'].values

selected_movie_name = st.selectbox(
     'Which Movie Would you like to see?',
     movie_list)

def fetch_poster(movie_id):
    movie_api_data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c85052c35838aa54c1a956e8a9a1c37a&language=en-US'.format(movie_id))

    data = movie_api_data.json()

    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']




def recommend(movie):
    movie_index = final_df[final_df['title'] == movie].index[0]
    similarity = similarity_distance[movie_index]
    movie_index_list = sorted(list(enumerate(similarity)),reverse=True,key=lambda x:x[1])[1:6]
    
    movie_list = []
    movie_id = []
    movie_poster_path = []

    for i in movie_index_list:
        movie_list.append(final_df.loc[i[0],'title'])
        movie_id.append(final_df.loc[i[0],'movie_id'])
        movie_poster_path.append(fetch_poster(final_df.loc[i[0],'movie_id']))

    return movie_list,movie_poster_path

if st.button('Recommend'):
    movie_list,movie_poster = recommend(selected_movie_name)

    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(movie_list[0])
        st.image(movie_poster[0])

    with col2:
        st.text(movie_list[1])
        st.image(movie_poster[1])

    with col3:
        st.text(movie_list[2])
        st.image(movie_poster[2])

    with col4:
        st.text(movie_list[3])
        st.image(movie_poster[3])

    with col5:
        st.text(movie_list[4])
        st.image(movie_poster[4])

