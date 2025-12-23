import joblib
from sentence_transformers import SentenceTransformer
import re

model = joblib.load("models/svm_best_model.pkl")
embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

SENTIMENTS = {0: "negative", 1: "neutral", 2: "positive"}

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def predict_sentiment(text):
    cleaned = clean_text(text)
    embedding = embedder.encode([cleaned])
    pred = model.predict(embedding)[0]
    return SENTIMENTS[pred]
