import streamlit as st
import pandas as pd
from src.data_loader import load_data
from src.content_based import ContentModel
from src.cold_start import ColdStartRecommender
import streamlit.components.v1 as components

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #080810 !important;
    color: #e0d9f5 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] { background: transparent !important; }

h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
}

h3, [data-testid="stSubheader"] > * {
    font-family: 'Syne', sans-serif !important;
    color: #b89aff !important;
}

/* Genre buttons */
div[data-testid="column"] button {
    background: #110d22 !important;
    border: 1px solid #2d2050 !important;
    color: #9480cc !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    width: 100% !important;
    transition: all 0.18s ease !important;
}
div[data-testid="column"] button:hover {
    background: #1e1440 !important;
    border-color: #7c4dff !important;
    color: #c9b3ff !important;
}

/* Primary / standalone buttons */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6a2fff, #9b4dff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    padding: 8px 28px !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #7c3fff, #b060ff) !important;
}

/* Multiselect */
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background: #110d22 !important;
    border: 1px solid #2d2050 !important;
    border-radius: 8px !important;
    color: #e0d9f5 !important;
}

/* Slider */
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {
    background: #7c4dff !important;
}
[data-testid="stSlider"] label {
    color: #9480cc !important;
    font-size: 13px !important;
}

label, .stMarkdown p { color: #9480cc !important; }

hr { border-color: #1e1640 !important; }

[data-testid="stAlert"] {
    background: #110d22 !important;
    border-color: #2d2050 !important;
    color: #b89aff !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080810; }
::-webkit-scrollbar-thumb { background: #2d2050; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")

# ---------- LOAD MODELS ----------
@st.cache_resource
def load_models():
    data, ratings, movies = load_data()

    content = ContentModel(data)
    content.train()

    cold_model = ColdStartRecommender(content)

    return data, ratings, movies, cold_model

data, ratings, movies, cold_model = load_models()

# ---------- GENRE NAVBAR ----------
st.subheader("🎭 Quick Genre Picks")

genres = [
    "Action", "Comedy", "Drama", "Romance",
    "Sci-Fi", "Horror", "Thriller", "Adventure"
]

cols = st.columns(len(genres))

selected_genre = None

for i, genre in enumerate(genres):
    if cols[i].button(genre):
        selected_genre = genre


# ---------- GENRE RECOMMEND FUNCTION ----------
def recommend_by_genre(movies, ratings, genre, top_n=5):
    genre_movies = movies[movies[genre] == 1]
    merged = pd.merge(genre_movies, ratings, on="item_id")

    top_movies = (
        merged.groupby("title")["rating"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    return top_movies


# ---------- CARD UI FUNCTION ----------
def show_movie_cards(movie_series):
    cols = st.columns(len(movie_series))

    for i, (movie, score) in enumerate(movie_series.items()):
        with cols[i]:
            components.html(
                f"""
                <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500&family=Syne:wght@600&display=swap" rel="stylesheet">
                <div style="
                    padding: 16px 12px;
                    border-radius: 12px;
                    background: linear-gradient(160deg, #1a1035, #110d22);
                    border: 1px solid #2d2050;
                    text-align: center;
                    min-height: 100px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    box-shadow: 0 4px 24px rgba(100, 50, 255, 0.08);
                ">
                    <div style="
                        color: #e0d9f5;
                        font-family: 'DM Sans', sans-serif;
                        font-size: 15px;
                        font-weight: 500;
                        overflow: hidden;
                        display: -webkit-box;
                        -webkit-line-clamp: 3;
                        -webkit-box-orient: vertical;
                        line-height: 1.35em;
                        height: 4.05em;
                    ">
                        {movie}
                    </div>
                    <div style="
                        color: #f5c518;
                        font-family: 'Syne', sans-serif;
                        font-size: 13px;
                        font-weight: 600;
                        letter-spacing: 0.3px;
                    ">
                        ⭐ {round(float(score), 2)}
                    </div>
                </div>
                """,
                height=180,
            )


# ---------- SHOW GENRE RESULTS ----------
if selected_genre:
    st.markdown(f"### 🎬 Top {selected_genre} Movies")
    genre_results = recommend_by_genre(movies, ratings, selected_genre)

    show_movie_cards(genre_results)


# ---------- COLD START ----------
st.markdown("---")
st.subheader("⭐ Personal Recommendations")

movie_list = movies['title'].unique()

selected_movies = st.multiselect(
    "Select movies you like",
    movie_list
)

user_ratings = {}

for movie in selected_movies:
    rating = st.slider(f"Rate {movie}", 1, 5, 3)
    user_ratings[movie] = rating


if st.button("Get Recommendations"):

    if len(user_ratings) < 2:
        st.warning("Please select at least 2 movies.")
    else:
        results = cold_model.recommend(user_ratings)

        st.markdown("### 🎯 Recommended for You")

        show_movie_cards(results)