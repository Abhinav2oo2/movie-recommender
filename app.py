import streamlit as st
import pickle
import pandas as pd
import time
import requests as rq
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = movies_list['title'].values

st.markdown("<h1 style='text-align:center;'>Movie Recommender System</h1>", unsafe_allow_html=True)
# st.title('Movie Recommender System')
Select_moviename = st.selectbox(
   "Enter A Movie to Recommend ",
   (movies),
   index=None,
   placeholder="Enter movie name...",
)

st.write('You selected:', Select_moviename)

def fetch_details(movie_id):
    response = rq.get('https://api.themoviedb.org/3/movie/{}?api_key=df04692b4790dd5b420a85e083a38d7b&language=en-US'.format(movie_id))
    data = response.json()
    return data['homepage']


def fetch_poster(movie_id):
   response=rq.get('https://api.themoviedb.org/3/movie/{}?api_key=df04692b4790dd5b420a85e083a38d7b&language=en-US'.format(movie_id))
   data=response.json()
   return "https://image.tmdb.org/t/p/original" +data['poster_path']

def recommend(movie_name):
   # if movie_name not in movies_list.keys():
   #  message=st.write("Searching the movie")
   movie_idx = movies_list[movies_list['title'] == movie_name].index[0]
   distance = similarity[movie_idx]
   movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
   recommedations =[]
   recommended_movieposters=[]
   movie_details =[]
   for i in movie_list:
      recommedations.append(movies_list.iloc[i[0]].title)
      recommended_movieposters.append(fetch_poster(movies_list.iloc[i[0]].movie_id))
      movie_details.append(fetch_details(movies_list.iloc[i[0]].movie_id))
   return recommedations, recommended_movieposters, movie_details

if st.button('Recommend'):
    if Select_moviename == None:
        st.warning(" :heavy_exclamation_mark: Please Enter the movie name")
        exit()
    with st.spinner('Wait for it...'):
        names, posters,detail_link= (recommend(Select_moviename))
        time.sleep(5)
    st.success('Done! Here is your movie recommendations:')
    if names == None or posters == None or detail_link == None:
        exit()

    num_columns = 5
    columns = st.columns(num_columns)
    #Iterate over columns and display images and text
    for i in range(num_columns):
        with columns[i]:
            st.image(posters[i])
            st.text(names[i])
            if detail_link[i] =='':
                st.warning("⚠️ Data is missing!.")
            else:
                st.link_button("Know more abt it...", detail_link[i])




# sidebar
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>Save your watchlist</h1>", unsafe_allow_html=True)
    with st.form("my_form",clear_on_submit=True,border=False):
        # st.write("Enter the Movie name")
        Select_moviename = st.selectbox(
            'Enter the Movie Name you watched',
            (movies),
            index=None,
            placeholder="Enter movie name...",
        )
        st.write("How Much You rate the Movie ?")
        slider_val = st.slider("Choose your value",min_value=0,max_value=5,step=1)
        answer = st.radio(
            "Will You suggest this Movie to your Friends?",
            [":rainbow[Yes]", "No"],
            index=None,
        )
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write( "Movie_name" , Select_moviename , "slider", slider_val, "checkbox", answer)
