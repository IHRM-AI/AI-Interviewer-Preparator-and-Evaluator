# Adaptive difficulty logic
# Current score aur difficulty level ke basis pe next difficulty decide karta hai

def next_difficulty(score, current):
    """
    Score aur current difficulty level ke basis pe next difficulty decide karta hai
    
    Args:
        score: Candidate ka current score (0-100)
        current: Current difficulty level (1, 2, ya 3)
    
    Returns:
        Next difficulty level (1, 2, ya 3)
    """
    # Agar score 80 se zyada hai to difficulty badhao
    # Maximum 3 tak ja sakta hai
    if score >= 80:
        return min(current + 1, 3)
    
    # Agar score 50 se kam hai to difficulty kam karo
    # Minimum 1 tak ja sakta hai
    elif score < 50:
        return max(current - 1, 1)
    
    # Agar beech mein hai to same difficulty rakho
    return current
