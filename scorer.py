# scorer.py
import re

def extract_keywords_from_text(text: str) -> set:
    """A helper function to clean a block of text and extract a set of unique keywords."""
    stop_words = {'a', 'an', 'the', 'and', 'in', 'on', 'for', 'with', 'to', 'of', 'is', 'it'}
    
    lower_text = text.lower()
    words = re.findall(r'\b[a-z0-9+#-]+\b', lower_text)

    # --- THE FIX IS HERE ---
    # Changed from len(word) > 2 to len(word) > 1 to include 2-letter skills like 'ai', 'go', 'c#', etc.
    return {word for word in words if word not in stop_words and len(word) > 1}


def hard_match_scorer(resume_text: str, jd_text: str) -> dict:
    """
    Compares a comma-separated JD skill list against keywords from the resume.
    """
    resume_keywords = extract_keywords_from_text(resume_text)
    jd_lower = jd_text.lower()
    jd_keywords = {skill.strip() for skill in jd_lower.split(',')}

    found_skills = list(jd_keywords.intersection(resume_keywords))
    
    score = 0
    if jd_keywords:
        score = (len(found_skills) / len(jd_keywords)) * 100
    
    # Debugging prints that appear in your backend terminal
    print("\n--- DEBUGGING INFO ---")
    print(f"JD Keywords Parsed: {jd_keywords}")
    print(f"Resume Keywords Found (sample): {list(resume_keywords)[:20]}")
    print(f"MATCHED SKILLS: {found_skills}")
    print(f"SCORE: {score}")
    print("----------------------\n")
    
    return {
        "score": round(score, 2),
        "matched_keywords": found_skills,
        "total_keywords_checked": list(jd_keywords)
    }