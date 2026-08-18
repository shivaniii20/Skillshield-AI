from Skill_gap import get_skill_gap

from Skill_matcher import (
    load_job_roles,
    extract_resume_skills,
    match_job_roles,
    get_top_roles
)

from course_recommender import (
    load_courses,
    recommend_courses
)


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

skills_file = "data/skills.csv"
job_roles_file = "data/job_roles.csv"
courses_file = "data/courses.csv"


# --------------------------------------------------
# LOAD DATASETS
# --------------------------------------------------

job_roles = load_job_roles(job_roles_file)
courses = load_courses(courses_file)


# --------------------------------------------------
# RESUME TEXT
# --------------------------------------------------

resume_text = """
BSc Data Science student with skills in Python, SQL,
Excel, Power BI, Tableau, Machine Learning,
Data Analysis and Data Visualization.
"""


# --------------------------------------------------
# EXTRACT RESUME SKILLS
# --------------------------------------------------

resume_skills = extract_resume_skills(
    resume_text,
    skills_file
)


print("\nDetected Resume Skills:")
print(", ".join(resume_skills))


# --------------------------------------------------
# MATCH RESUME WITH ALL JOB ROLES
# --------------------------------------------------

results_df = match_job_roles(
    resume_skills,
    job_roles
)


# --------------------------------------------------
# GET TOP 3 JOB ROLES
# --------------------------------------------------

top_roles = get_top_roles(
    results_df,
    top_n=3
)


print("\n" + "=" * 70)
print("TOP 3 JOB ROLE RECOMMENDATIONS")
print("=" * 70)


# --------------------------------------------------
# ANALYZE TOP 3 ROLES
# --------------------------------------------------

for rank, (_, row) in enumerate(
    top_roles.iterrows(),
    start=1
):

    print(f"\n{'#' * 70}")
    print(f"#{rank}  {row['job_role']}")
    print(f"{'#' * 70}")

    print(f"\nCategory: {row['category']}")
    print(f"Match Score: {row['match_score']}%")


    # ----------------------------------------------
    # MATCHED SKILLS
    # ----------------------------------------------

    print("\nMatched Skills:")

    if row["matched_skills"]:
        for skill in row["matched_skills"].split(", "):
            print("  ✓", skill)
    else:
        print("  None")


    # ----------------------------------------------
    # MISSING SKILLS
    # ----------------------------------------------

    print("\nMissing Skills:")

    if row["missing_skills"]:
        missing_skills = row["missing_skills"].split(", ")

        for skill in missing_skills:
            print("  ✗", skill)

    else:
        missing_skills = []
        print("  None")


    # ----------------------------------------------
    # SKILL GAP
    # ----------------------------------------------

    if row["missing_skills"]:
        
        required_skills = (
            row["matched_skills"] + ", " +
            row["missing_skills"]
        )

        gap_result = get_skill_gap(
            resume_skills,
            required_skills
        )

        print(
            f"\nSkill Gap: "
            f"{gap_result['gap_percentage']}%"
        )

    else:

        print("\nSkill Gap: 0%")


    # ----------------------------------------------
    # COURSE RECOMMENDATIONS
    # ----------------------------------------------

    print("\nRecommended Courses:")

    if missing_skills:

        recommendations = recommend_courses(
            missing_skills,
            courses
        )

        if recommendations.empty:

            print("  No courses found.")

        else:

            for _, course in recommendations.iterrows():

                print(
                    f"\n  📚 {course['course']}"
                )

                print(
                    f"     Skill: {course['skill']}"
                )

                print(
                    f"     Platform: "
                    f"{course['platform']}"
                )

                print(
                    f"     Level: "
                    f"{course['level']}"
                )

                print(
                    f"     Duration: "
                    f"{course['duration']}"
                )

    else:

        print("  No courses required.")


    print("\n" + "-" * 70)