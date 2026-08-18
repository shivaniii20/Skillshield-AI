def get_skill_gap(resume_skills, required_skills):
    """
    Compare resume skills with job role requirements
    and identify matched and missing skills.
    """

    # Convert resume skills to lowercase
    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    # Convert required skills to lowercase
    required_skills = {
        skill.lower().strip()
        for skill in required_skills.split(",")
    }

    # Find matched and missing skills
    matched_skills = resume_skills.intersection(required_skills)
    missing_skills = required_skills - resume_skills

    # Calculate gap percentage
    if len(required_skills) > 0:
        gap_percentage = (
            len(missing_skills) / len(required_skills)
        ) * 100
    else:
        gap_percentage = 0

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "gap_percentage": round(gap_percentage, 2)
    }