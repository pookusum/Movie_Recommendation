# 🎬 Movie Recommendation System

🔗 **Live Demo:** https://movierecommendation-icgafb3yznm6dkbappwtibt.streamlit.app 

---

## 📌 About the Project

Ever wondered *“What should I watch next?”* 🤔  

This project is a **Movie Recommendation System** that suggests similar movies based on your selection. It uses machine learning techniques to analyze movie data and recommend the most relevant options.

The goal was to build something simple, interactive, and practical — and deploy it so anyone can use it in real time.

---

## 🚀 Features

- 🎥 Select a movie and get instant recommendations  
- 🧠 Content-based filtering using similarity scores  
- ⚡ Fast and interactive UI built with Streamlit  
- 🌐 Fully deployed web app (accessible anywhere)  
- 📦 Handles large model files using external hosting (Hugging Face)

---

## 🛠️ Tech Stack

- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **Streamlit**
- **Hugging Face (for hosting large `.pkl` files)**

---

## ⚙️ How It Works

1. Movie data is processed and converted into feature vectors  
2. Cosine similarity is calculated between movies  
3. When a user selects a movie:
   - The system finds similar movies
   - Returns top 5 recommendations  

---

## 📂 Project Structure
├── app.py
├── requirements.txt
├── movie_dict.pkl
├── similarity.pkl
├── tmdb_5000_movies.csv
└── README.md



---

## ▶️ Run Locally

```bash
git clone 
cd your-repo
pip install -r requirements.txt
streamlit run app.py
