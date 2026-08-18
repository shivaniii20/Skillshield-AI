from course_recommender import load_courses, recommend_courses


# File path
courses_file = "data/courses.csv"


# Load courses
courses_df = load_courses(courses_file)


# Test missing skills
missing_skills = [
    "statistics",
    "matplotlib",
    "python"
]


# Get recommendations
recommendations = recommend_courses(
    missing_skills,
    courses_df
)


print("\n" + "=" * 70)
print("COURSE RECOMMENDATIONS")
print("=" * 70)


if recommendations.empty:
    print("\nNo courses found.")
else:

    for _, row in recommendations.iterrows():

        print(f"\nSkill: {row['skill']}")
        print(f"Course: {row['course']}")
        print(f"Platform: {row['platform']}")
        print(f"Level: {row['level']}")
        print(f"Duration: {row['duration']}")

        print("-" * 70)