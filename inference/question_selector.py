import json
import random
from functools import lru_cache
from pathlib import Path

# File ke location se absolute paths banaye
BASE_DIR = Path(__file__).parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "interview_questions.json"

DIFFICULTY_MAP = {
    1: "Easy",
    2: "Medium",
    3: "Hard",
}


def _normalize(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
    return value if value else None


def _norm_key(value):
    value = _normalize(value)
    return value.lower() if isinstance(value, str) else value


def _normalize_difficulty(difficulty, score=None):
    if difficulty is None and score is not None:
        if score >= 80:
            difficulty = 3
        elif score < 50:
            difficulty = 1
        else:
            difficulty = 2

    if isinstance(difficulty, int):
        return DIFFICULTY_MAP.get(difficulty)
    if isinstance(difficulty, str):
        d = difficulty.strip().lower()
        if d in ("easy", "e"):
            return "Easy"
        if d in ("medium", "med", "m"):
            return "Medium"
        if d in ("hard", "h"):
            return "Hard"
    return None


def _iter_records():
    # Prefer streaming parser if available for large files
    try:
        import ijson  # type: ignore
        with open(RAW_PATH, "r", encoding="utf-8") as f:
            for item in ijson.items(f, "item"):
                yield item
        return
    except Exception:
        pass

    # Fallback: load entire JSON (may be heavy for large datasets)
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        yield item


def _minimal_item(item):
    return {
        "question": item.get("question"),
        "ideal_answer": item.get("ideal_answer"),
        "category": item.get("category"),
        "role": item.get("role"),
        "experience": item.get("experience"),
        "difficulty": item.get("difficulty"),
        "source_type": item.get("source_type"),
        "keywords": item.get("keywords"),
    }


def _matches(item, role_key=None, exp_key=None, categories_key=None):
    if role_key and _norm_key(item.get("role")) != role_key:
        return False
    if exp_key and _norm_key(item.get("experience")) != exp_key:
        return False
    if categories_key:
        if _norm_key(item.get("category")) not in categories_key:
            return False
    return True


@lru_cache(maxsize=128)
def _get_pool(role_key, exp_key, categories_key_tuple):
    categories_key = set(categories_key_tuple) if categories_key_tuple else None
    pool = []

    for item in _iter_records():
        if _matches(item, role_key, exp_key, categories_key):
            pool.append(_minimal_item(item))

    return pool


def generate_next_question(
    role=None,
    experience=None,
    categories=None,
    difficulty=None,
    score=None,
    asked_questions=None,
):
    role_key = _norm_key(role)
    exp_key = _norm_key(experience)
    categories_key_tuple = None
    if categories:
        categories_key_tuple = tuple(sorted({_norm_key(c) for c in categories if _normalize(c)}))

    pool = _get_pool(role_key, exp_key, categories_key_tuple)
    if not pool:
        return None

    asked = set([q for q in (asked_questions or []) if q])
    diff = _normalize_difficulty(difficulty, score=score)

    def _pick(candidates):
        return random.choice(candidates) if candidates else None

    # 1) Match difficulty + not asked
    if diff:
        candidates = [q for q in pool if q.get("difficulty") == diff and q.get("question") not in asked]
        picked = _pick(candidates)
        if picked:
            return picked

    # 2) Ignore difficulty, not asked
    candidates = [q for q in pool if q.get("question") not in asked]
    picked = _pick(candidates)
    if picked:
        return picked

    # 3) Allow repeat, match difficulty if possible
    if diff:
        candidates = [q for q in pool if q.get("difficulty") == diff]
        picked = _pick(candidates)
        if picked:
            return picked

    # 4) Fallback: any from pool
    return _pick(pool)
