# 🎬 Hybrid Movie Recommendation System using Machine Learning & TMDB API

## 📌 Overview

This project is an **AI/ML-based hybrid movie recommendation system** that combines **content-based filtering** with **real-time data from TMDB API** to deliver personalized and dynamic movie suggestions.

It supports both:

* 📂 Local dataset-based recommendations (ML)
* 🌐 Live movie recommendations from TMDB API

---

## 🚀 Features

* 🤖 Content-based recommendation using **TF-IDF & Cosine Similarity**
* 🌐 Real-time movie data using **TMDB API**
* ⭐ Smart ranking using **rating + popularity score**
* 🎭 Genre-based filtering
* 📅 Displays **release year**
* 🌍 Shows **language**
* 🖼 Movie **poster URLs**
* 📈 Trending movies section
* 🔄 Fetches large-scale movie data (thousands of movies)
* ⚡ Handles errors and network issues gracefully

---

## 🧠 Tech Stack

* **Python**
* **Pandas**
* **Scikit-learn**
* **Requests**
* **RapidFuzz**
* **TMDB API**

---

## 📂 Project Structure

```
movie-recommendation-system/
│
├── app.py                # Main application
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── dataset.csv          # Optional dataset
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Add your TMDB API Key

Replace in code:

```
API_KEY = "YOUR_API_KEY"
```

Get API key from: https://www.themoviedb.org/

---

## ▶️ How to Run

```
python app.py
```

---

## 🧪 Usage

* Enter movie name (optional)
* Enter genre (e.g., Action, Horror, Comedy)
* Set minimum rating
* Get recommended movies with:

  * Title
  * Rating
  * Score
  * Year
  * Language
  * Poster

---

## 📊 Example Output

```
Title           Rating   Score   Year   Language
------------------------------------------------
The Shining      8.2     5.7     1980   English
Get Out          7.6     5.3     2017   English
...
```

---

## 📈 Future Improvements

* 🎨 Streamlit Web UI (Netflix-style interface)
* 🖼 Poster grid display
* 🔍 Advanced filters (year, language, popularity)
* 🤖 Collaborative filtering (user-based recommendations)
* 🌐 Deployment on cloud

---

## 💼 Resume Description

Developed a hybrid movie recommendation system using **machine learning (TF-IDF, cosine similarity)** integrated with **TMDB API**, delivering real-time personalized recommendations from large-scale movie datasets.

---

## 📜 License

This project is for educational and learning purposes.

---

## 🙌 Acknowledgements

* TMDB API for movie data
* Scikit-learn for ML algorithms
