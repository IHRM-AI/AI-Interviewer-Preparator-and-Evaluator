# Question selector jo difficulty level ke basis pe questions select karta hai

def select_question(questions, difficulty_level):
    """
    Difficulty level ke basis pe appropriate question select karta hai
    
    Args:
        questions: List of questions with difficulty info
        difficulty_level: Current difficulty level (1, 2, ya 3)
    
    Returns:
        Selected question dictionary
    """
    # Filter questions by difficulty level
    filtered = [q for q in questions if q.get("difficulty", 2) == difficulty_level]
    
    # Agar koi question nahi mila to default difficulty 2 wala lo
    if not filtered:
        filtered = [q for q in questions if q.get("difficulty", 2) == 2]
    
    # Agar phir bhi nahi mila to pehla question de do
    if not filtered:
        return questions[0] if questions else None
    
    # Random question select karo filtered list se
    import random
    return random.choice(filtered)
