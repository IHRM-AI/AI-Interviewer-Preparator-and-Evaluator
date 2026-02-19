import json
import re
from functools import lru_cache
from pathlib import Path

# File ke location se absolute paths banaye
BASE_DIR = Path(__file__).parent.parent
RAW_PATH = BASE_DIR / "data" / "raw" / "interview_questions.json"
CACHE_PATH = BASE_DIR / "data" / "processed" / "metadata.json"

DIFFICULTY_ORDER = {
    "Easy": 0,
    "Medium": 1,
    "Hard": 2,
}


def _difficulty_key(value: str):
    return (DIFFICULTY_ORDER.get(value, 99), value)


def _experience_key(value: str):
    v = value.strip().lower()
    if "fresher" in v:
        return (0, 0, v)
    nums = re.findall(r"\d+", v)
    if nums:
        return (1, int(nums[0]), v)
    return (2, 0, v)


def _normalize(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
    return value if value else None


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


def _load_cache():
    if not CACHE_PATH.exists():
        return None
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_cache(metadata):
    try:
        CACHE_PATH.parent.mkdir(exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=True, indent=2)
    except Exception:
        # Cache write fail ho to API ko block mat karo
        pass


def _compute_metadata():
    categories = set()
    difficulties = set()
    experiences = set()
    roles = set()

    for item in _iter_records():
        cat = _normalize(item.get("category"))
        diff = _normalize(item.get("difficulty"))
        exp = _normalize(item.get("experience"))
        role = _normalize(item.get("role"))

        if cat:
            categories.add(cat)
        if diff:
            difficulties.add(diff)
        if exp:
            experiences.add(exp)
        if role:
            roles.add(role)

    metadata = {
        "categories": sorted(categories),
        "difficulties": sorted(difficulties, key=_difficulty_key),
        "experiences": sorted(experiences, key=_experience_key),
        "roles": sorted(roles),
    }
    return metadata


@lru_cache(maxsize=1)
def get_metadata():
    cached = _load_cache()
    if cached:
        return cached

    metadata = _compute_metadata()
    _save_cache(metadata)
    return metadata
