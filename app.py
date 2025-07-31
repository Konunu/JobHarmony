import numpy as np
import random
import re

# Mock job database (same as original)
jobs = [
    {"title": "AI Engineer", "skills": ["Python", "Machine Learning", "TensorFlow", "Data Analysis"], "personality_fit": {"Openness": 8, "Conscientiousness": 7, "Extraversion": 5, "Agreeableness": 6, "Neuroticism": 3}, "description": "Build AI models for innovative apps."},
    {"title": "Data Scientist", "skills": ["Python", "SQL", "Statistics", "Visualization"], "personality_fit": {"Openness": 7, "Conscientiousness": 8, "Extraversion": 4, "Agreeableness": 5, "Neuroticism": 4}, "description": "Analyze data to drive business decisions."},
    {"title": "Product Manager", "skills": ["Project Management", "Communication", "Agile", "User Research"], "personality_fit": {"Openness": 6, "Conscientiousness": 9, "Extraversion": 8, "Agreeableness": 7, "Neuroticism": 2}, "description": "Lead product development teams."},
    {"title": "UX Designer", "skills": ["Figma", "User Experience", "Prototyping", "Research"], "personality_fit": {"Openness": 9, "Conscientiousness": 6, "Extraversion": 7, "Agreeableness": 8, "Neuroticism": 3}, "description": "Design intuitive user interfaces."},
]

# Skills taxonomy (same)
skills_taxonomy = {
    "Technical": ["Python", "SQL", "Machine Learning", "Data Analysis", "TensorFlow"],
    "Soft": ["Communication", "Project Management", "Teamwork", "Problem Solving"],
    "Transferable Maps": {
        "Python": ["Programming", "Scripting", "Automation"],
        "Communication": ["Public Speaking", "Writing", "Negotiation"]
    }
}

# Comfort messages (same, abbreviated)
comforting_messages = [
    "You're doing great—job hunting is tough, but your persistence will pay off.",
    "Take a deep breath; remember, every 'no' is closer to a 'yes'.",
    "Your skills are unique; the right opportunity is out there.",
    "Feeling overwhelmed? Focus on one application at a time.",
    "You've got this—celebrate small wins like updating your resume."
]

# Big Five questions (same)
big_five_questions = {
    "Openness": ["I am open to new experiences.", "I have a vivid imagination.", "I enjoy abstract ideas.", "I prefer routine over variety."],
    "Conscientiousness": ["I am organized and dependable.", "I pay attention to details.", "I follow through on tasks.", "I sometimes procrastinate."],
    "Extraversion": ["I am outgoing and energetic.", "I enjoy social gatherings.", "I talk a lot.", "I prefer solitude."],
    "Agreeableness": ["I am compassionate and cooperative.", "I trust others easily.", "I avoid arguments.", "I can be critical of others."],
    "Neuroticism": ["I worry a lot.", "I get stressed easily.", "I am moody.", "I remain calm under pressure."]
}

def extract_skills(text):
    extracted = set()
    for category, skills in skills_taxonomy.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                extracted.add(skill)
    transferables = {}
    for skill in extracted:
        if skill in skills_taxonomy["Transferable Maps"]:
            transferables[skill] = skills_taxonomy["Transferable Maps"][skill]
    return extracted, transferables

def match_jobs(user_skills, personality_scores):
    matches = []
    for job in jobs:
        skill_match = len(user_skills.intersection(set(job["skills"]))) / len(job["skills"]) if job["skills"] else 0
        personality_match = np.mean([abs(personality_scores[trait] - job["personality_fit"][trait]) for trait in personality_scores]) / 10
        overall_score = (skill_match * 0.6) + ((1 - personality_match) * 0.4)
        if overall_score > 0.5:
            matches.append((job, overall_score, skill_match, personality_match))
    return sorted(matches, key=lambda x: x[1], reverse=True)

def generate_advice(personality_scores):
    advice = []
    if personality_scores["Openness"] > 6: advice.append("Your high openness suits creative roles like design or innovation.")
    if personality_scores["Conscientiousness"] > 7: advice.append("Leverage your organization in management positions.")
    return advice

# Simulated run with hardcoded inputs
personality_responses = {
    "Openness": [5, 4, 5, 2],  # High
    "Conscientiousness": [4, 5, 4, 2],  # High
    "Extraversion": [3, 4, 3, 3],  # Moderate
    "Agreeableness": [4, 4, 5, 2],  # High
    "Neuroticism": [3, 3, 4, 4]  # Moderate
}

# Calculate scores
scores = {}
for trait, res in personality_responses.items():
    rev_last = 6 - res[-1]  # Reverse last
    scores[trait] = np.mean(res[:-1] + [rev_last]) * 2  # Scale to 10

print("Personality Scores:", scores)
print("Career Advice:", generate_advice(scores))

# Skills input
resume_text = "Experienced in Python, Machine Learning, and strong Communication skills. Background in data analysis."
user_skills, transferables = extract_skills(resume_text)
print("\nDetected Skills:", user_skills)
print("Transferable Skills:", transferables)

# Job matching
matches = match_jobs(user_skills, scores)
print("\nRecommended Jobs:")
for job, score, skill_m, pers_m in matches:
    print(f"- {job['title']} (Score: {round(score*100)}%)")
    print(f"  Description: {job['description']}")
    print(f"  Why: Skills match {round(skill_m*100)}%, Personality fit {round((1-pers_m)*100)}%. E.g., Your Python/ML align with building models; high openness fits innovation.")

# Comfort chat simulation
user_feeling = "I'm feeling stressed about not getting callbacks."
ack = "Stress can be tough. Take a deep breath—here's something to help:"
message = random.choice(comforting_messages)
print("\nComfort Response:", ack, message)
