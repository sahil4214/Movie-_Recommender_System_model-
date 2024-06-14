import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your movie dataset
movies = pd.read_csv('Movielist.csv')

# Fill NaN values with an empty string
movies['cast'] = movies['cast'].fillna('')
movies['crew'] = movies['crew'].fillna('')

# Combine relevant features into a single string
movies['combined_features'] = movies['cast'] + " " + movies['crew']

# Create a TF-IDF vectorizer and compute the similarity matrix
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Ensure the 'model' directory exists
os.makedirs('model', exist_ok=True)

# Save the movies DataFrame and similarity matrix to pickle files
with open('model/movie_list.pkl', 'wb') as f:
    pickle.dump(movies, f)

with open('model/similarity.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)
