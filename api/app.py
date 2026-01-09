from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sys
from pathlib import Path

# Parent directory ko path mein add karo taaki inference module import ho sake
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from inference.score_answer import score_answer
from inference.adaptive_logic import next_difficulty
from inference.analytics import generate_report

# FastAPI app banaye
app = FastAPI()

# Exception handler - agar koi error aaye to properly handle karega
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": type(exc).__name__}
    )

# Request models - yeh data validation ke liye use hote hain
class ScoreRequest(BaseModel):
    question: str
    ideal_answer: str
    user_answer: str

class DifficultyRequest(BaseModel):
    score: float
    current_difficulty: int

class AnalyticsRequest(BaseModel):
    scores: List[float]

# Root endpoint - just to check if API is running
@app.get("/")
def root():
    return {"message": "Interview Scoring API is running"}

# Answer scoring endpoint
@app.post("/score")
def score(data: ScoreRequest):
    """
    Question, ideal answer aur user answer ko score karta hai
    """
    try:
        score_value = score_answer(
            data.question,
            data.ideal_answer,
            data.user_answer
        )
        
        return {
            "score": score_value
        }
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__
        }

# Adaptive difficulty endpoint
@app.post("/next_difficulty")
def get_next_difficulty(data: DifficultyRequest):
    """
    Current score aur difficulty ke basis pe next difficulty suggest karta hai
    """
    next_diff = next_difficulty(
        data.score,
        data.current_difficulty
    )
    
    return {
        "next_difficulty": next_diff
    }

# Analytics endpoint
@app.post("/analytics")
def get_analytics(data: AnalyticsRequest):
    """
    All scores ke basis pe overall report generate karta hai
    """
    report = generate_report(data.scores)
    
    return report
