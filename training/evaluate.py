import pandas as pd
import joblib
from tensorflow.keras.models import load_model

DATA_DIR = "../data/processed"
MODEL_DIR = "../model"

# Validation data load karo
val = pd.read_csv(f"{DATA_DIR}/val.csv")

# Same combine function jo training mein use kiya tha
def combine(row):
    return row["question"] + " " + row["ideal_answer"] + " " + row["candidate_answer"]

# Saved vectorizer ko load karo
vectorizer = joblib.load(f"{DATA_DIR}/tfidf_vectorizer.pkl")

# Validation text ko vectors mein convert karo
X_val = vectorizer.transform(val.apply(combine, axis=1))
y_val = val["label"].values

# Trained model ko load karo
# compile=False use kiya hai kyunki Keras 3.x mein compatibility issue hai
from tensorflow.keras.optimizers import Adam
model = load_model(f"{MODEL_DIR}/answer_scorer.h5", compile=False)
# Model ko manually compile karo same settings ke saath
model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])

# Model ko evaluate karo validation data pe
# Loss aur MAE dono return hoga
loss, mae = model.evaluate(X_val.toarray(), y_val)

# MAE (Mean Absolute Error) dikhaye
# Yeh batata hai ki average mein kitna error hai predictions mein
print(f"Validation MAE: {mae:.4f}")
