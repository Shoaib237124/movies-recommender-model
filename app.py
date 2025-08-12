import streamlit as st
import pickle
import requests
import ast
import os
import urllib.request
import gdown

file_id = "1hRT38pzmOWU-McJPbFXwdw37QxyDKrYu"
output = "cosine_similarity.pkl"
url = f"https://drive.google.com/uc?id={file_id}"

if not os.path.exists(output):
    print("Downloading cosine_similarity.pkl with gdown...")
    gdown.download(url, output, quiet=False)






def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_movie_details(selected_movie):
    """Get detailed information about the selected movie from Combined_Movies.pkl"""
    # Find the movie in the combined dataset
    movie_row = combined_movies[combined_movies['title'] == selected_movie]
    
    if movie_row.empty:
        # Fallback to basic info if not found in combined dataset
        return {
            'title': selected_movie,
            'movie_id': None,
            'genres': [],
            'cast': [],
            'crew': [],
            'overview': "No overview available"
        }
    
    movie_row = movie_row.iloc[0]
    
    # Get all the detailed information from the combined dataset
    details = {
        'title': movie_row['title'],
        'movie_id': movie_row['movie_id']
    }
    
    # Add genres if available
    if 'genres' in movie_row:
        if isinstance(movie_row['genres'], list):
            details['genres'] = movie_row['genres']
        else:
            # If genres is stored as string, try to convert it
            try:
                details['genres'] = ast.literal_eval(movie_row['genres'])
            except:
                details['genres'] = []
    else:
        details['genres'] = []
    
    # Add cast if available
    if 'cast' in movie_row:
        if isinstance(movie_row['cast'], list):
            details['cast'] = movie_row['cast']
        else:
            try:
                details['cast'] = ast.literal_eval(movie_row['cast'])
            except:
                details['cast'] = []
    else:
        details['cast'] = []
    
    # Add crew/director if available
    if 'crew' in movie_row:
        if isinstance(movie_row['crew'], list):
            details['crew'] = movie_row['crew']
        else:
            try:
                details['crew'] = ast.literal_eval(movie_row['crew'])
            except:
                details['crew'] = []
    else:
        details['crew'] = []
    
    # Add overview if available - convert list to string if needed
    if 'overview' in movie_row:
        overview = movie_row['overview']
        if isinstance(overview, list):
            # Convert list of words back to readable string
            details['overview'] = ' '.join(overview)
        else:
            details['overview'] = overview
    else:
        details['overview'] = "No overview available"
    
    return details

def get_movie_details_for_recommendations(movie_title):
    """Get movie details for recommended movies from Combined_Movies.pkl"""
    movie_row = combined_movies[combined_movies['title'] == movie_title]
    
    if movie_row.empty:
        return {
            'genres': [],
            'cast': [],
            'overview': "No overview available"
        }
    
    movie_row = movie_row.iloc[0]
    
    # Extract genres
    genres = []
    if 'genres' in movie_row:
        if isinstance(movie_row.genres, list):
            genres = movie_row.genres
        else:
            try:
                genres = ast.literal_eval(movie_row.genres)
            except:
                genres = []
    
    # Extract cast
    cast = []
    if 'cast' in movie_row:
        if isinstance(movie_row.cast, list):
            cast = movie_row.cast
        else:
            try:
                cast = ast.literal_eval(movie_row.cast)
            except:
                cast = []
    
    # Extract overview - convert list to string if needed
    overview = "No overview available"
    if 'overview' in movie_row:
        overview_data = movie_row.overview
        if isinstance(overview_data, list):
            # Convert list of words back to readable string
            overview = ' '.join(overview_data)
        else:
            overview = overview_data
    
    return {
        'genres': genres,
        'cast': cast,
        'overview': overview
    }

def recommend_movies(selected_movie):
    """Get recommendations using the processed tags from movies_recommendation.pkl"""
    movie_index = movies_list[movies_list['title'] == selected_movie].index[0]
    distances = cosine_sim[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_genres = []
    recommended_movies_cast = []
    recommended_movies_overview = []
    
    for i in movie_list:
        movie_title = movies_list.iloc[i[0]].title
        movie_id = movies_list.iloc[i[0]].movie_id
        
        # Get detailed info from Combined_Movies.pkl
        movie_details = get_movie_details_for_recommendations(movie_title)
        
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_genres.append(movie_details['genres'])
        recommended_movies_cast.append(movie_details['cast'])
        recommended_movies_overview.append(movie_details['overview'])
    
    return recommended_movies, recommended_movies_posters, recommended_movies_genres, recommended_movies_cast, recommended_movies_overview

# Load both datasets
movies_list = pickle.load(open('movies_recommendation.pkl', 'rb'))  # For recommendations
combined_movies = pickle.load(open('Combined_Movies.pkl', 'rb'))    # For detailed info
cosine_sim = pickle.load(open('cosine_similarity.pkl', 'rb'))      # For similarity matrix

# Streamlit UI
st.set_page_config(page_title="Movie Recommender System", layout="wide")
st.title('🎬 Movie Recommender System')

# Movie selection
selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies_list['title'].values
)

if st.button('🎯 Get Recommendations'):
    # Get selected movie details
    movie_details = get_movie_details(selected_movie_name)
    
    # Display selected movie details
    st.header(f"🎭 {movie_details['title']}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if movie_details['movie_id']:
            poster_url = fetch_poster(movie_details['movie_id'])
            st.image(poster_url, width=300)
        else:
            st.write("Poster not available")
    
    with col2:
        # Display overview
        st.subheader("📖 Overview")
        st.write(movie_details['overview'])
        
        # Display genres if found
        if movie_details['genres']:
            st.subheader("🎭 Genres")
            genres_text = ", ".join(movie_details['genres'])
            st.write(genres_text)
        else:
            st.subheader("🎭 Genres")
            st.write("Genres not available")
        
        # Display cast if found
        if movie_details['cast']:
            st.subheader("👥 Cast")
            cast_text = ", ".join(movie_details['cast'])
            st.write(cast_text)
        else:
            st.subheader("👥 Cast")
            st.write("Cast not available")
        
        # Display director if found
        if movie_details['crew']:
            st.subheader("🎬 Director")
            crew_text = ", ".join(movie_details['crew'])
            st.write(crew_text)
        else:
            st.subheader("🎬 Director")
            st.write("Director not available")
    
    st.markdown("---")
    
    # Get and display recommendations
    st.header("🎯 Similar Movies You Might Like")
    recommended_movies, recommended_movies_posters, recommended_movies_genres, recommended_movies_cast, recommended_movies_overview = recommend_movies(selected_movie_name)
    
    # Display recommendations in a grid
    cols = st.columns(5)
    
    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movies_posters[i], width=150)
            st.subheader(recommended_movies[i])
            
            # Show genres if found
            if recommended_movies_genres[i]:
                st.caption("Genres:")
                genres_display = ", ".join(recommended_movies_genres[i][:3])  # Show first 3 genres
                st.write(genres_display)
            
            # Show cast if found
            if recommended_movies_cast[i]:
                st.caption("Cast:")
                cast_display = ", ".join(recommended_movies_cast[i][:2])  # Show first 2 cast members

                st.write(cast_display)



