# Analytics functions jo interview ke baad report generate karte hain

def generate_report(scores):
    """
    Scores ke basis pe overall report generate karta hai
    
    Args:
        scores: List of scores jo candidate ne har question pe achieve kiye
    
    Returns:
        Dictionary with overall score, strength, aur recommendation
    """
    # Average score calculate karo
    overall_score = round(sum(scores)/len(scores), 2)
    
    # Strength determine karo average score ke basis pe
    if overall_score > 70:
        strength = "Conceptual clarity"
    else:
        strength = "Needs improvement"
    
    # Recommendation de
    recommendation = "Practice structured answers"
    
    return {
        "overall_score": overall_score,
        "strength": strength,
        "recommendation": recommendation
    }
