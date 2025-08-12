# TMDB Movie Recommender System

[![Streamlit App](https://img.shields.io/badge/Streamlit-Deployed-green)](https://movies-recommender-model-dnvj5jc8pkpj3ue2rjw4cs.streamlit.app/)

---

## Project Overview

This project is a movie recommendation system built using the **TMDB (The Movie Database) dataset** sourced from Kaggle. The system recommends movies based on similarity, allowing users to select a movie and receive detailed information along with a list of similar movies they might enjoy.

---

## Features

- **Data Preprocessing & Vectorization:**  
  Cleaned and preprocessed the TMDB dataset, extracting relevant features such as genres, cast, crew, and more. Applied text vectorization using `CountVectorizer`.

- **Cosine Similarity Model:**  
  Developed a recommendation model based on cosine similarity between movies, enabling the system to find and suggest 5 similar movies for each selection.

- **Interactive Frontend with Streamlit:**  
  Built a user-friendly web interface where users can:  
  - Search and select a movie  
  - View detailed movie information including title, poster, genre, cast, and crew  
  - Get 5 recommended similar movies displayed with the same details

- **Deployment:**  
  The app is deployed and live on [Streamlit Cloud](https://movies-recommender-model-dnvj5jc8pkpj3ue2rjw4cs.streamlit.app/), making it easily accessible online.

---

## Tech Stack

- **Python:** Data preprocessing, model development  
- **Pandas & NumPy:** Dataset manipulation  
- **Scikit-learn:** Text vectorization and cosine similarity calculations  
- **Streamlit:** Frontend UI and deployment  
- **Pickle:** Serialization of preprocessed data and similarity matrix


 Visit the live app here:  
   [TMDB Movie Recommender](https://movies-recommender-model-dnvj5jc8pkpj3ue2rjw4cs.streamlit.app/)

s.txt
streamlit run app.py
