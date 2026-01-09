import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

DATA_DIR = "../data/processed"

# Training data load karo
train = pd.read_csv(f"{DATA_DIR}/train.csv")

# Question, ideal answer aur candidate answer ko combine karo
# Yeh important hai kyunki model ko context chahiye
def combine(row):
    return row["question"] + " " + row["ideal_answer"] + " " + row["candidate_answer"]

train_text = train.apply(combine, axis=1)

# TF-IDF vectorizer banaye
# Max features 30000 rakha hai taaki memory efficient ho
# Stop words hata diye hain English ke
vectorizer = TfidfVectorizer(
    max_features=30000,
    stop_words="english"
)

# Text ko numbers mein convert karo (vectors)
X = vectorizer.fit_transform(train_text)

# Vectorizer aur features ko save karo taaki baad mein use kar sakein
joblib.dump(vectorizer, f"{DATA_DIR}/tfidf_vectorizer.pkl")
joblib.dump(X, f"{DATA_DIR}/X_train.pkl")
joblib.dump(train["label"].values, f"{DATA_DIR}/y_train.pkl")

print("TF-IDF features saved")
