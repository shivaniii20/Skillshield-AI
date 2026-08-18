import pandas as pd


def load_courses(file_path):
    """Load course dataset."""

    courses_df = pd.read_csv(file_path)

    return courses_df


def recommend_courses(missing_skills, courses_df, courses_per_skill=2):
    """Recommend courses based on missing skills."""

    recommendations = []

    # Handle missing skills given as a string
    if isinstance(missing_skills, str):

        missing_skills = [
            skill.strip()
            for skill in missing_skills.split(",")
            if skill.strip()
        ]

    # Handle missing skills given as a list/set
    else:

        missing_skills = [
            str(skill).strip()
            for skill in missing_skills
            if str(skill).strip()
        ]

    # Clean course dataset skill column
    courses_df["skill_clean"] = (
        courses_df["skill"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Match each missing skill
    for skill in missing_skills:

        skill_clean = skill.lower().strip()

        matching_courses = courses_df[
            courses_df["skill_clean"] == skill_clean
        ]

        matching_courses = matching_courses.head(
            courses_per_skill
        )

        for _, row in matching_courses.iterrows():

            recommendations.append({
                "skill": row["skill"],
                "course": row["course"],
                "platform": row["platform"],
                "level": row["level"],
                "duration": row["duration"]
            })

    return pd.DataFrame(recommendations)