import streamlit as st
import pandas as pd
import numpy as np
import difflib
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Premium Commercial Cinematic UI Configuration
st.set_page_config(page_title="CinemAI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for Professional Commercial Look
st.markdown("""
    <style>
    .stApp { background-color: #090d16; }
    .movie-card {
        background: linear-gradient(145deg, #151f32, #0d1624);
        padding: 24px; border-radius: 16px; border: 1px solid #1e293b;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); margin-bottom: 20px;
    }
    .movie-title { color: #ffffff; font-size: 24px; font-weight: 700; margin-bottom: 10px; }
    .movie-genre-badge {
        background-color: rgba(56, 189, 248, 0.1); color: #38bdf8;
        padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 600;
        display: inline-block; margin-bottom: 12px;
    }
    .movie-plot { color: #94a3b8; font-size: 14px; line-height: 1.5; margin-bottom: 15px; }
    .movie-rating { color: #fbbf24; font-weight: bold; font-size: 16px; }
    .history-item {
        background-color: #151f32; padding: 10px 15px; border-radius: 8px;
        margin-bottom: 8px; border-left: 4px solid #38bdf8; color: #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_production_catalog():
    path = "movies_metadata.csv"
    df = pd.read_csv(path, low_memory=False)
    movies = df[['title', 'genres', 'overview', 'vote_average', 'vote_count']].copy()
    movies['overview'] = movies['overview'].fillna('')
    movies['title'] = movies['title'].fillna('Untitled Production')
    
    def extract_genres(x):
        try:
            g_list = ast.literal_eval(x)
            return " ".join([d['name'] for d in g_list]) if g_list else 'General'
        except: return 'General'
            
    movies['genres_list'] = movies['genres'].astype(str).apply(extract_genres)
    
    # 🧠 WEIGHTED SEARCH CORPUS: We repeat genres and title to make them more important than the plot
    # This ensures Godzilla gives monsters, not just San Francisco movies.
    movies['search_corpus'] = (movies['genres_list'] + " ") * 3 + (movies['title'] + " ") * 2 + movies['overview']
    
    C = movies['vote_average'].mean()
    m = 50
    movies['final_score'] = (movies['vote_count']/(movies['vote_count'] + m)) * movies['vote_average'] + (m/(movies['vote_count'] + m)) * C
    return movies.sort_values('vote_count', ascending=False).head(8000).reset_index(drop=True)

movies = load_production_catalog()

if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []

with st.sidebar:
    st.markdown("## 👤 User Space")
    st.markdown("---")
    st.markdown("### 🕒 Recent Watch History")
    if st.session_state['search_history']:
        for h in reversed(st.session_state['search_history'][-5:]):
            st.markdown(f'<div class="history-item">🎬 {h}</div>', unsafe_allow_html=True)
        if st.button("Clear History Log"):
            st.session_state['search_history'] = []
            st.rerun()
    else: st.caption("No recent activity.")

# Branding Update: Just "CinemAI"
st.markdown("<h1 style='color: white; font-size: 42px;'>CinemAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 16px;'>Discover, analyze, and instantly track your next favorite cinematic production experience.</p>", unsafe_allow_html=True)
st.markdown("---")

user_search = st.text_input("Search Engine", value="", placeholder="Search for a movie title")

confirmed_title = None
if user_search:
    all_titles = movies['title'].astype(str).tolist()
    matches = difflib.get_close_matches(user_search, all_titles, n=5, cutoff=0.25)
    if matches:
        confirmed_title = st.selectbox("🎯 Select exact match discovered:", matches)
        if confirmed_title and (not st.session_state['search_history'] or st.session_state['search_history'][-1] != confirmed_title):
            st.session_state['search_history'].append(confirmed_title)
    else: st.error("No matches discovered.")

st.markdown("### 🔥 Handpicked Recommendations Tailored For You")

if confirmed_title:
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['search_corpus'])
    target_idx = movies[movies['title'] == confirmed_title].index[0]
    
    cosine_sim = linear_kernel(tfidf_matrix[target_idx], tfidf_matrix).flatten()
    # Sort and pick top matches
    sim_indices = cosine_sim.argsort()[::-1][1:5] 
    results = movies.iloc[sim_indices]
    
    grid_col1, grid_col2 = st.columns(2)
    for i, row in enumerate(results.itertuples()):
        col = grid_col1 if i % 2 == 0 else grid_col2
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">{row.title}</div>
                    <div class="movie-genre-badge">{" • ".join(row.genres_list.split())}</div>
                    <div class="movie-plot">{row.overview[:180]}...</div>
                    <div class="movie-rating">⭐ {round(row.vote_average, 1)} / 10</div>
                </div>
            """, unsafe_allow_html=True)
            
            clean_name = row.title.replace(" ", "+")
            yt = f"https://www.youtube.com/results?search_query={clean_name}+official+trailer"
            gs = f"https://www.google.com/search?q=watch+{clean_name}+online"
            
            b1, b2 = st.columns(2)
            b1.markdown(f'<a href="{yt}" target="_blank"><button style="width:100%; background-color:#ef4444; color:white; border:none; padding:8px; border-radius:6px; font-weight:600; cursor:pointer;">▶ Play Official Trailer</button></a>', unsafe_allow_html=True)
            b2.markdown(f'<a href="{gs}" target="_blank"><button style="width:100%; background-color:#1e293b; color:#e2e8f0; border:1px solid #334155; padding:8px; border-radius:6px; font-weight:600; cursor:pointer;">🔍 Stream Movie</button></a>', unsafe_allow_html=True)
            st.write("")
else:
    # Professional user guidance
    st.info("💡 Search for a title above to discover custom tailored recommendations.")