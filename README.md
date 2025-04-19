# movie-recommender

Check it out -> https://recommendmemovie.streamlit.app/

![image](https://github.com/user-attachments/assets/4c780856-01f6-4b3c-b207-4cf6a3e8b56c)

This project is a content-based movie recommender system built using Python, Streamlit, and machine learning techniques. It suggests movies similar to a selected title by analyzing textual metadata such as genre, cast, crew, and keywords. The app is deployed using Streamlit Community Cloud, with large file storage managed via Hugging Face Hub.

### Key Features:
- Content-Based Filtering: Recommends movies based on similarity in metadata, not user ratings.
- Cosine Similarity: Computes movie-to-movie similarity using NLP techniques.
- Poster Fetching: Retrieves movie posters dynamically using the TMDb API.
- Lightweight Web Interface: Built using Streamlit for interactive recommendations.
- Large File Handling: Hosts .pkl files on Hugging Face and loads them remotely using Python.

### Tech Stack:
Layer | Tool/Library
Frontend | Streamlit
Backend | Python
ML/NLP | scikit-learn, pandas
Deployment | Streamlit Cloud + GitHub
File Hosting | Hugging Face Hub

### Technologies/concepts used:
Component | Technology / Concept
Language | Python
Data Handling | pandas, numpy
NLP Vectorization | scikit-learn CountVectorizer
Similarity Calculation | cosine similarity from scikit-learn
Web App Framework | Streamlit
Deployment | Streamlit Cloud + GitHub
Large File Hosting | Hugging Face Hub (for similarity.pkl)
Poster API | TMDb API

### Workflow:

#### 1. Dataset Acquisition and Pre-processing

Dataset Used: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
tmdb_5000_movies.xlsx – contains movie overviews, genres, and production info
tmdb_5000_credits.xlsx – includes cast and crew data for each movie

Merging & Cleaning:
- Merged both datasets on the title column to create a single cohesive dataframe.
- Dropped unnecessary columns like production companies, release dates, and budget that weren’t used in similarity scoring.
- Checked for and removed duplicate entries and handled null values.
   
#### 2. Feature Engineering and Count Representation

Extracted Features:
- Genres: Converted list of dictionaries into flat strings (e.g., ["Action", "Adventure"] → "action adventure")
- Cast: Extracted top 3 leading actors for each movie.
- Crew: Extracted only the Director (using role filtering).
- Keywords: Used provided tags/keywords associated with the plot or theme.

Tag Consolidation:
- Concatenated all the above into a single unified tags field: tags = genre + cast + director + keywords + overview

Text Preprocessing:
- Converted text to lowercase
- Removed spaces between multi-word names using tokenization (e.g., "Robert Downey Jr." → "robertdowneyjr")
- Removed punctuation and performed basic normalization
- Applied stemming to reduce words to their base/root form

#### 3. NLP Vectorization & Similarity Computation

Vectorization:
- Used CountVectorizer from scikit-learn
- Created a sparse matrix (document-term matrix) where:
Each row = a movie
Each column = a unique token/word from the top 5000 words across all tags
Cell values = token frequency in a movie’s tag string

Cosine Similarity:
- Applied cosine similarity to measure how closely each movie's tag vector matches another
- Cosine similarity score ranges from 0 to 1:
1 = identical vector direction (perfect match)
0 = orthogonal vectors (completely dissimilar)
- Results in a symmetric similarity matrix where: similarity[i][j] = similarity between movie i and movie j, Matrix shape: n x n, where n = number of movies
  
#### 4. Recommendation Logic

When a user selects a movie:
- Find its index in the dataframe
- Retrieve corresponding similarity scores from the similarity matrix
- Sort all other movies in descending order of similarity score
- Exclude the movie itself from the recommendations
- Select top N movies (usually 5–10)
- Display recommended movie titles along with their posters
   
#### 5. Poster Retrieval via TMDb API

To enhance visual appeal, the app fetches movie posters using the TMDb API:
- Each movie in the dataset has a unique movie_id
- A GET request is sent to TMDb’s /movie/{id} endpoint
- The API returns JSON with metadata, including a poster_path
    
#### 6. Deployment

Given that similarity.pkl exceeds GitHub’s 100 MB limit, a two-part deployment strategy was implemented:

i. Large File Hosting (Hugging Face Hub)
- The file was uploaded to a public Hugging Face Hub repository.
- In the Streamlit app, it is downloaded at runtime

ii. Deployment (Streamlit Community Cloud)
- Code is version-controlled and hosted on GitHub.
- The app is deployed directly from the GitHub repo via Streamlit Cloud.
- The following were configured: requirements.txt: Lists dependencies, app.py: Main script, .gitignore: Excludes large .pkl files from version control

iii. Performance Optimization
- Used @st.cache_data in Streamlit to cache the remote file after the first download
- Avoids repeated network calls and speeds up app responsiveness

### Learning Highelights:

- Practical application of NLP techniques in recommendation systems
- Using cosine similarity for vector-based comparisons
- Managing large files outside GitHub using modern tools
- Streamlit caching and deployment best practices
- Understanding of the end-to-end deployment lifecycle

### Future Scope:

- Improve recommendation logic with TF-IDF or hybrid collaborative filtering
- Add search functionality or filters (genre, year, etc.)
