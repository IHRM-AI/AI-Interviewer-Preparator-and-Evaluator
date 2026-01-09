import joblib
from tensorflow.keras.callbacks import EarlyStopping
from model import build_model

DATA_DIR = "../data/processed"
MODEL_DIR = "../model"

# Pehle se saved features aur labels ko load karo
X = joblib.load(f"{DATA_DIR}/X_train.pkl")
y = joblib.load(f"{DATA_DIR}/y_train.pkl")

# Model banaye input dimension ke saath
model = build_model(X.shape[1])

# Early stopping callback - agar validation loss improve nahi ho raha to training stop kar dega
# Patience 1 means ek epoch wait karega improvement ke liye
early_stop = EarlyStopping(patience=1, monitor="val_loss", restore_best_weights=True)

# Model ko train karo
# 3 epochs tak train karega
# Batch size 1024 hai taaki fast training ho
# 10% data validation ke liye use hoga
model.fit(
    X.toarray(),
    y,
    epochs=3,
    batch_size=1024,
    validation_split=0.1,
    callbacks=[early_stop]
)

# Trained model ko save karo
model.save(f"{MODEL_DIR}/answer_scorer.h5")
print("Model trained and saved")
