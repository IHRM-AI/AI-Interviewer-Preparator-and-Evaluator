# Interview Answer Scoring System

Yeh project interview answers ko automatically score karta hai using machine learning.

## Setup

Pehle requirements install karo:

```bash
pip install -r requirements.txt
```

## Execution Order (IMPORTANT)

Files ko sirf isi order mein run karo:

### Step 1: Data Preprocessing
```bash
cd training
python prepare_data.py
```

Yeh `data/raw/interview_question.json` ko read karke `data/processed/train.csv` aur `data/processed/val.csv` banayega.

### Step 2: Feature Extraction
```bash
python feature_extraction.py
```

Yeh text ko TF-IDF vectors mein convert karega aur save karega.

### Step 3: Model Training
```bash
python train.py
```

Yeh neural network model ko train karega aur `model/answer_scorer.h5` mein save karega.

### Step 4: Model Evaluation
```bash
python evaluate.py
```

Yeh validation data pe model ko test karega aur MAE score dikhayega.

### Step 5: API Server
```bash
cd ../api
uvicorn app:app --reload
```

API server start ho jayega. Endpoints:

- `POST /score` - Answer ko score karta hai
- `POST /next_difficulty` - Next difficulty level suggest karta hai
- `POST /analytics` - Overall report generate karta hai

## Project Structure

```
SANSAL-AI Interview/
├── data/
│   ├── raw/
│   │   └── interview_question.json
│   └── processed/
│       ├── train.csv
│       ├── val.csv
│       └── tfidf_vectorizer.pkl
├── model/
│   └── answer_scorer.h5
├── training/
│   ├── prepare_data.py
│   ├── feature_extraction.py
│   ├── model.py
│   ├── train.py
│   └── evaluate.py
├── inference/
│   ├── score_answer.py
│   ├── question_selector.py
│   ├── adaptive_logic.py
│   └── analytics.py
├── api/
│   ├── app.py
│   └── routes.py
├── requirements.txt
└── README.md
```

## Notes

- Har file ko sequentially run karna zaroori hai
- Model training ke baad hi inference use kar sakte ho
- API server ko inference files ke saath use karo
# SANSAL--AI-Interview
