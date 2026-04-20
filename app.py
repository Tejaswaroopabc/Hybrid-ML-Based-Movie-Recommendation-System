import pandas as pd
import requests
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ==============================
# 🔐 API KEY
# ==============================
API_KEY = "YOUR_API_KEY_HERE"

# ==============================
# 🌐 SESSION + RETRY
# ==============================
session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)

headers = {"User-Agent": "Mozilla/5.0"}

# ==============================
# 🌍 LANGUAGE MAP
# ==============================
LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "ko": "Korean",
    "fr": "French",
    "ja": "Japanese",
    "es": "Spanish",
    "zh": "Chinese",
    "it": "Italian",
    "de": "German"
}

# ==============================
# 📂 LOAD DATASET
# ==============================
file_path = input("Enter dataset path (CSV) or press Enter to skip: ")

if file_path:
    df = pd.read_csv(file_path)
    print("✅ Dataset Loaded:", df.shape)
else:
    df = None
    print("⚠ WEB-ONLY mode")

# ==============================
# 🔍 COLUMN DETECTION
# ==============================
def find_column(df, keywords):
    for col in df.columns:
        for key in keywords:
            if key.lower() in col.lower():
                return col
    return None

if df is not None:
    title_col = find_column(df, ['title', 'movie', 'name'])
    genre_col = find_column(df, ['genre'])
    rating_col = find_column(df, ['rating', 'vote'])
    text_col = find_column(df, ['overview', 'description'])

    df.drop_duplicates(inplace=True)
    df[text_col] = df[text_col].fillna("")

    df['combined'] = df[text_col] if not genre_col else df[genre_col] + " " + df[text_col]

    tfidf = TfidfVectorizer(stop_words='english')
    matrix = tfidf.fit_transform(df['combined'])
    similarity = cosine_similarity(matrix)

# ==============================
# ⭐ RANKING FUNCTION
# ==============================
def compute_score(rating, popularity):
    return (0.7 * rating) + (0.3 * (popularity / 100))

# ==============================
# 🎭 GENRE CACHE
# ==============================
GENRE_CACHE = None

def get_genre_id(genre_name):
    global GENRE_CACHE

    if GENRE_CACHE is None:
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}"
        GENRE_CACHE = session.get(url, headers=headers).json().get('genres', [])

    for g in GENRE_CACHE:
        if genre_name.lower() == g['name'].lower():
            return g['id']
    return None

# ==============================
# 🌐 FETCH MAX MOVIES (NO LIMIT)
# ==============================
def fetch_web_movies(genre, min_rating=0):
    movies = []

    try:
        genre_id = get_genre_id(genre) if genre else None

        page = 1
        MAX_PAGES = 500

        while page <= MAX_PAGES:
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&page={page}"

            if genre_id:
                url += f"&with_genres={genre_id}"

            response = session.get(url, headers=headers, timeout=10)
            data = response.json()

            results = data.get('results', [])

            if not results:
                print("✅ No more movies available.")
                break

            for m in results:
                if m['vote_average'] >= min_rating:
                    score = compute_score(m['vote_average'], m['popularity'])

                    movies.append({
                        'title': m['title'],
                        'rating': m['vote_average'],
                        'popularity': m['popularity'],
                        'score': score,
                        'year': m['release_date'][:4] if m.get('release_date') else "N/A",
                        'language': LANG_MAP.get(m.get('original_language'), m.get('original_language', 'N/A')),
                        'poster': f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m['poster_path'] else "N/A",
                        'source': 'web'
                    })

            print(f"📄 Fetched page {page}")

            page += 1
            time.sleep(0.4)

        print(f"\n🎯 Total movies collected: {len(movies)}")

        df_movies = pd.DataFrame(movies)
        return df_movies.sort_values(by="score", ascending=False)

    except Exception as e:
        print("⚠ Web error:", e)
        return pd.DataFrame()

# ==============================
# 🔥 TRENDING
# ==============================
def get_trending():
    try:
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={API_KEY}"
        data = session.get(url, headers=headers).json()

        movies = []
        for m in data.get('results', []):
            movies.append({
                "title": m['title'],
                "rating": m['vote_average'],
                "year": m['release_date'][:4] if m.get('release_date') else "N/A",
                "language": LANG_MAP.get(m.get('original_language'), 'N/A'),
                "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}"
            })

        return pd.DataFrame(movies)

    except:
        return pd.DataFrame()

# ==============================
# 🎬 LOCAL RECOMMENDER
# ==============================
def local_recommend(movie_name=None, top_n=10):
    if df is None or not movie_name:
        return pd.DataFrame()

    best_match = process.extractOne(movie_name, df[title_col].tolist())
    if not best_match:
        return pd.DataFrame()

    idx = df[df[title_col] == best_match[0]].index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    return pd.DataFrame({
        'title': [df.iloc[i[0]][title_col] for i in scores],
        'source': 'local'
    })

# ==============================
# 🔗 HYBRID SYSTEM
# ==============================
def hybrid_recommend(movie, genre, rating):
    local = local_recommend(movie)
    web = fetch_web_movies(genre, rating)

    final = pd.concat([local, web], ignore_index=True)

    return final

# ==============================
# 🧑‍💻 USER MENU
# ==============================
while True:
    print("\n===== 🎬 FINAL MOVIE RECOMMENDER =====")
    print("1. Recommend Movies")
    print("2. Trending Movies")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        movie = input("Movie name (optional): ")
        genre = input("Genre: ")
        rating = float(input("Min rating: ") or 0)

        results = hybrid_recommend(movie, genre, rating)

        print("\n🎯 RESULTS:\n")
        print(results[['title', 'rating', 'score', 'year', 'language', 'source']])

    elif choice == "2":
        print("\n🔥 TRENDING MOVIES:\n")
        print(get_trending())

    elif choice == "3":
        break