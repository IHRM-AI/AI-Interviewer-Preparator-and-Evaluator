import joblib
from tensorflow.keras.models import load_model
from pathlib import Path

# File ke location se absolute paths banaye
# Yeh ensure karega ki paths sahi rahein chahe kahan se import ho
BASE_DIR = Path(__file__).parent.parent
VEC_PATH = BASE_DIR / "data" / "processed" / "tfidf_vectorizer.pkl"
MODEL_PATH = BASE_DIR / "model" / "answer_scorer.h5"

# Global variables for lazy loading
vectorizer = None
model = None

# Model aur vectorizer ko load karne ka function
# Lazy loading - pehli baar call pe load hoga
def _load_models():
    global vectorizer, model
    if vectorizer is None or model is None:
        vectorizer = joblib.load(str(VEC_PATH))
        # compile=False use kiya hai Keras 3.x compatibility ke liye
        # Prediction ke liye compile ki zarurat nahi hai
        model = load_model(str(MODEL_PATH), compile=False)

# Answer ko score karne ka function
# Question, ideal answer aur user ka answer lega
# Score return karega 0 se 100 ke beech mein
def score_answer(question, ideal_answer, user_answer):
    # Pehle models load karo agar nahi load hue hain
    _load_models()
    
    # Sabko combine karo taaki context mile
    text = question + " " + ideal_answer + " " + user_answer
    
    # Text ko vector mein convert karo
    X = vectorizer.transform([text])
    
    # Model se prediction lo
    # Sigmoid output hai jo 0-1 ke beech mein hoga
    score = model.predict(X.toarray(), verbose=0)[0][0]
    
    # Score ko 0-100 scale mein convert karo aur round off karo
    return round(score * 100, 2)
