import pandas as pd
import re

def load_job_roles(file_path):
    """Load job roles and required skills from CSV."""
    df = pd.read_csv(file_path)
    return df


def extract_resume_skills(resume_text, skills_file):
    """Find skills from the resume text using the master skills dataset."""

    skills_df = pd.read_csv(skills_file)

    resume_text = resume_text.lower()

    detected_skills = []

    for skill in skills_df["skill"]:

        skill_pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(skill_pattern, resume_text):
            detected_skills.append(skill)

    return list(set(detected_skills))


def calculate_match(resume_skills, required_skills):
    """Calculate job-role match percentage."""

    resume_skills = {skill.lower().strip() for skill in resume_skills}

    required = {
        skill.lower().strip()
        for skill in required_skills.split(",")
    }

    matched = resume_skills.intersection(required)
    missing = required - resume_skills

    if len(required) == 0:
        score = 0
    else:
        score = (len(matched) / len(required)) * 100

    return round(score, 2), matched, missing


def match_job_roles(resume_skills, job_roles_df):
    """Match resume skills against all available job roles."""

    results = []

    for _, row in job_roles_df.iterrows():

        score, matched, missing = calculate_match(
            resume_skills,
            row["required_skills"]
        )

        results.append({
            "job_role": row["job_role"],
            "category": row["category"],
            "match_score": score,
            "matched_skills": ", ".join(sorted(matched)),
            "missing_skills": ", ".join(sorted(missing))
        })

    results_df = pd.DataFrame(results)

    return results_df.sort_values(
        by="match_score",
        ascending=False
    )

def match_job_roles(resume_skills, job_roles_df):
    """Match resume skills against all available job roles."""

    results = []

    for _, row in job_roles_df.iterrows():

        score, matched, missing = calculate_match(
            resume_skills,
            row["required_skills"]
        )

        results.append({
            "job_role": row["job_role"],
            "category": row["category"],
            "match_score": score,
            "matched_skills": ", ".join(sorted(matched)),
            "missing_skills": ", ".join(sorted(missing))
        })

    results_df = pd.DataFrame(results)

    return results_df.sort_values(
        by="match_score",
        ascending=False
    )


def get_top_roles(results_df, top_n=3):
    """Return the top recommended job roles."""

    return results_df.head(top_n)