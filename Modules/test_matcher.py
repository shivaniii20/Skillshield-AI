from Skill_matcher import (
    load_job_roles,
    extract_resume_skills,
    match_job_roles
)

# File paths
skills_file = "data/skills.csv"
job_roles_file = "data/job_roles.csv"

# Load job roles
job_roles = load_job_roles(job_roles_file)

# Test resume text
resume_text = """
BSc Data Science student with skills in Python, SQL,
Excel, Power BI, Tableau, Machine Learning,
Data Analysis and Data Visualization.
"""

# Extract skills
skills = extract_resume_skills(
    resume_text,
    skills_file
)

print("\nDetected Skills:")
print(skills)

# Match job roles
results = match_job_roles(
    skills,
    job_roles
)

print("\nJob Role Recommendations:")
print(results.head(10).to_string(index=False))
