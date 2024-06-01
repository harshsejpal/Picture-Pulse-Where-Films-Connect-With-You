#app.py
import streamlit as st
import pickle
import requests

st.set_page_config(page_title="Harsh's Movie Recommendations")

# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key='
#                  '8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key='
                 '8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data.get('poster_path')  # Check if 'poster_path' exists in the response
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None  # Return None if 'poster_path' is not available


def recommend(movie, movies_df, similarity):
    movie_index = movies_df[movies_df['title'].str.lower() == movie.lower()].index
    if len(movie_index) == 0:
        print("Movie not found.")
        return []
    movie_index = movie_index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        #fetch poster from API
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_df = pickle.load(open('movies.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('PicturePulse: Where Films Connect with You')

selected_movie = st.selectbox(
    'Discover your next favourite film!', movies_df['title'].values)

# if st.button('Recommend'):
#     names, posters = recommend(selected_movie, movies_df, similarity)
#     cols = st.columns(5)
#
#     for i in range(5):  # Iterate over the range of values from 0 to 4
#         with cols[i]:
#             st.text(names[i])
#             st.image(posters[i])
#             st.markdown("---")

if st.button('Recommend'):
    names, posters = recommend(selected_movie, movies_df, similarity)
    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]  # Define a list of columns
    for i in range(min(len(names), len(cols))):  # Iterate over the minimum of names and cols
        if posters[i]:  # Check if the poster is not None
            with cols[i]:  # Use the corresponding column
                st.header(names[i])
                st.image(posters[i])
                st.markdown("---")
        else:
            print(f"Poster not available for {names[i]}")
