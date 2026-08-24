import streamlit as st
import pandas as pd
import os
import sys


# ============================================================
# MODULE PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODULES_DIR = os.path.join(
    BASE_DIR,
    "Modules"
)

if MODULES_DIR not in sys.path:
    sys.path.append(MODULES_DIR)


# ============================================================
# IMPORT BACKEND
# ============================================================

from resume_parser import extract_text_from_pdf

from Skill_matcher import (
    extract_resume_skills,
    load_job_roles,
    match_job_roles,
    get_top_roles
)

from Skill_gap import get_skill_gap

from course_recommender import (
    load_courses,
    recommend_courses
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SkillShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ SkillShield AI")

    st.caption(
        "AI-Powered Career Intelligence"
    )

    st.divider()

    st.subheader("📌 Dashboard")

    st.write("📝 Resume Analysis")
    st.write("🎯 Career Matching")
    st.write("📈 Skill Gap Analysis")
    st.write("📚 Learning Roadmap")

    st.divider()

    st.caption(
        "SkillShield AI • Resume Intelligence System"
    )


# ============================================================
# PREMIUM HERO
# ============================================================

with st.container(
    border=True
):

    hero_left, hero_right = st.columns(
        [4, 1]
    )

    with hero_left:

        st.markdown(
            "# 🛡️ SkillShield AI"
        )

        st.subheader(
            "AI-Powered Career Intelligence"
        )

        st.write(
            "Your Resume. Your Skills. Your Career Roadmap."
        )

        st.caption(
            "Transform your resume into a personalized career "
            "strategy. Discover your strengths, identify career "
            "opportunities, uncover skill gaps and build a focused "
            "learning roadmap."
        )

    with hero_right:

        st.metric(
            "🎯 Career Analysis",
            "AI Ready"
        )

        st.caption(
            "Resume → Skills → Career → Learning"
        )


st.divider()


# ============================================================
# FILE PATHS
# ============================================================

SKILLS_FILE = os.path.join(
    BASE_DIR,
    "Data",
    "skills.csv"
)

JOB_ROLES_FILE = os.path.join(
    BASE_DIR,
    "Data",
    "Job_roles.csv"
)

COURSES_FILE = os.path.join(
    BASE_DIR,
    "Data",
    "courses.csv"
)

# ============================================================
# UPLOAD SECTION
# ============================================================

st.header(
    "📄 Start Your Career Analysis"
)

st.caption(
    "Upload your latest PDF resume to generate your personalized career dashboard."
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)


if uploaded_file is None:

    st.info(
        "👆 Upload your PDF resume to start your SkillShield AI analysis."
    )

    st.stop()


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze My Resume",
    use_container_width=True
):

    temp_file = os.path.join(
        BASE_DIR,
        "uploaded_resume.pdf"
    )

    with open(
        temp_file,
        "wb"
    ) as f:

        f.write(
            uploaded_file.getbuffer()
        )


    try:

        # ====================================================
        # 1. RESUME EXTRACTION
        # ====================================================

        with st.spinner(
            "📄 Reading and analyzing your resume..."
        ):

            resume_text = extract_text_from_pdf(
                temp_file
            )


        if not resume_text.strip():

            st.error(
                "Unable to extract text from the resume."
            )

            st.stop()


        # ====================================================
        # 2. SKILL DETECTION
        # ====================================================

        with st.spinner(
            "🧠 Detecting your skills..."
        ):

            detected_skills = extract_resume_skills(
                resume_text,
                SKILLS_FILE
            )


        # ====================================================
        # 3. LOAD DATASETS
        # ====================================================

        with st.spinner(
            "📊 Loading career intelligence data..."
        ):

            job_roles_df = load_job_roles(
                JOB_ROLES_FILE
            )

            courses_df = load_courses(
                COURSES_FILE
            )


        # ====================================================
        # 4. CAREER MATCHING
        # ====================================================

        with st.spinner(
            "🎯 Finding your best career matches..."
        ):

            results_df = match_job_roles(
                detected_skills,
                job_roles_df
            )

            top_roles = get_top_roles(
                results_df,
                top_n=3
            )


        if top_roles.empty:

            st.warning(
                "No suitable career roles were found."
            )

            st.stop()


        # ====================================================
        # 5. TOP ROLE
        # ====================================================

        top_role = top_roles.iloc[0]


        top_role_data = job_roles_df[
            job_roles_df["job_role"]
            == top_role["job_role"]
        ]


        required_skills = top_role_data[
            "required_skills"
        ].iloc[0]


        # ====================================================
        # 6. SKILL GAP
        # ====================================================

        top_role_gap = get_skill_gap(
            detected_skills,
            required_skills
        )


        # ====================================================
        # 7. CALCULATE METRICS
        # ====================================================

        total_skills = len(
            detected_skills
        )

        top_score = float(
            top_role["match_score"]
        )

        gap_score = float(
            top_role_gap["gap_percentage"]
        )


        readiness = round(
            (
                top_score * 0.65
            )
            +
            (
                (100 - gap_score) * 0.35
            )
        )


        readiness = max(
            0,
            min(
                100,
                readiness
            )
        )


        # ====================================================
        # 8. CAREER SNAPSHOT
        # ====================================================

        st.header(
            "📊 Your Career Snapshot"
        )

        st.caption(
            "A quick overview of your current career profile."
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "🧠 Skills Detected",
                total_skills
            )


        with col2:

            st.metric(
                "🎯 Top Match",
                f"{top_score:.1f}%"
            )


        with col3:

            st.metric(
                "💼 Best-Fit Role",
                top_role["job_role"]
            )


        with col4:

            st.metric(
                "🚀 Career Readiness",
                f"{readiness}%"
            )


        # ====================================================
        # 9. PERSONALIZED INSIGHT
        # ====================================================

        if top_score >= 80:

            insight = (
                f"Your profile has a strong alignment with "
                f"{top_role['job_role']}. Focus on strengthening "
                f"the remaining gaps and building practical projects."
            )

        elif top_score >= 60:

            insight = (
                f"You have a promising foundation for "
                f"{top_role['job_role']}. Closing the identified "
                f"skill gaps can significantly improve your match."
            )

        else:

            insight = (
                f"Your profile is still developing for "
                f"{top_role['job_role']}. Follow the learning roadmap "
                f"to build the most important missing skills."
            )


        st.info(
            f"💡 **SkillShield Personalized Insight**\n\n{insight}"
        )


        # ====================================================
        # 10. CAREER READINESS
        # ====================================================

        st.header(
            "🚀 Career Readiness Progress"
        )

        st.caption(
            "Your estimated readiness based on career alignment and skill coverage."
        )


        progress_col1, progress_col2 = st.columns(
            [5, 1]
        )


        with progress_col1:

            st.progress(
                readiness / 100
            )


        with progress_col2:

            st.metric(
                "Readiness",
                f"{readiness}%"
            )


        # ====================================================
        # 11. DETECTED SKILLS
        # ====================================================

        st.header(
            "🧠 Your Detected Skills"
        )

        st.caption(
            "Skills identified directly from your uploaded resume."
        )


        if detected_skills:

            skill_columns = st.columns(3)


            for index, skill in enumerate(
                sorted(detected_skills)
            ):

                with skill_columns[
                    index % 3
                ]:

                    st.success(
                        f"✓ {skill}"
                    )

        else:

            st.warning(
                "No skills were detected from this resume."
            )


        # ====================================================
        # 12. CAREER PATH ANALYSIS
        # ====================================================

        st.header(
            "🎯 Career Path Analysis"
        )

        st.caption(
            "See how your current skill profile aligns with potential career paths."
        )


        chart_df = results_df[
            [
                "job_role",
                "match_score"
            ]
        ].head(8).copy()


        chart_df = chart_df.set_index(
            "job_role"
        )


        st.bar_chart(
            chart_df,
            use_container_width=True
        )


        # ====================================================
        # 13. CAREER RECOMMENDATIONS
        # ====================================================

        st.header(
            "💼 Recommended Career Paths"
        )

        st.caption(
            "Your strongest career options based on your detected skills."
        )


        for index, (_, row) in enumerate(
            top_roles.iterrows(),
            start=1
        ):

            with st.container(
                border=True
            ):

                role_col1, role_col2 = st.columns(
                    [4, 1]
                )


                with role_col1:

                    st.subheader(
                        f"#{index} {row['job_role']}"
                    )

                    st.caption(
                        f"{row['category']}"
                    )


                with role_col2:

                    st.metric(
                        "Match",
                        f"{float(row['match_score']):.1f}%"
                    )


                st.divider()


                matched = [
                    skill.strip()
                    for skill in str(
                        row["matched_skills"]
                    ).split(",")
                    if skill.strip()
                ]


                missing = [
                    skill.strip()
                    for skill in str(
                        row["missing_skills"]
                    ).split(",")
                    if skill.strip()
                ]


                skill_col1, skill_col2 = st.columns(2)


                with skill_col1:

                    st.markdown(
                        "#### ✅ Matched Skills"
                    )


                    if matched:

                        for skill in matched:

                            st.success(
                                skill
                            )

                    else:

                        st.caption(
                            "No matched skills listed."
                        )


                with skill_col2:

                    st.markdown(
                        "#### 📌 Skills To Develop"
                    )


                    if missing:

                        for skill in missing:

                            st.warning(
                                skill
                            )

                    else:

                        st.success(
                            "No major missing skills!"
                        )


        # ====================================================
        # 14. SKILL GAP ANALYSIS
        # ====================================================

        st.header(
            "📈 Skill Gap Analysis"
        )

        st.caption(
            "Understand what is helping your match and what still needs development."
        )


        matched_skills = top_role_gap[
            "matched_skills"
        ]


        missing_skills = top_role_gap[
            "missing_skills"
        ]


        # ----------------------------------------------------
        # Normalize matched skills
        # ----------------------------------------------------

        if isinstance(
            matched_skills,
            str
        ):

            matched_skills = [
                skill.strip()
                for skill in matched_skills.split(",")
                if skill.strip()
            ]

        elif isinstance(
            matched_skills,
            (list, tuple, set)
        ):

            matched_skills = [
                str(skill).strip()
                for skill in matched_skills
                if str(skill).strip()
            ]

        else:

            matched_skills = []


        # ----------------------------------------------------
        # Normalize missing skills
        # ----------------------------------------------------

        if isinstance(
            missing_skills,
            str
        ):

            missing_skills = [
                skill.strip()
                for skill in missing_skills.split(",")
                if skill.strip()
            ]

        elif isinstance(
            missing_skills,
            (list, tuple, set)
        ):

            missing_skills = [
                str(skill).strip()
                for skill in missing_skills
                if str(skill).strip()
            ]

        else:

            missing_skills = []


        # ====================================================
        # GAP SUMMARY
        # ====================================================

        gap_col1, gap_col2 = st.columns(
            [1, 2]
        )


        with gap_col1:

            st.metric(
                "📉 Skill Gap",
                f"{gap_score:.1f}%"
            )

            st.metric(
                "✅ Matched Skills",
                len(matched_skills)
            )

            st.metric(
                "📌 Missing Skills",
                len(missing_skills)
            )


        with gap_col2:

            gap_data = pd.DataFrame({

                "Status": [
                    "Matched Skills",
                    "Missing Skills"
                ],

                "Count": [
                    len(matched_skills),
                    len(missing_skills)
                ]

            })


            st.bar_chart(
                gap_data.set_index(
                    "Status"
                ),
                use_container_width=True
            )


        # ====================================================
        # 15. PRIORITY SKILLS
        # ====================================================

        if missing_skills:

            st.subheader(
                "🎯 Priority Skills To Build"
            )


            priority_columns = st.columns(3)


            for index, skill in enumerate(
                missing_skills
            ):

                with priority_columns[
                    index % 3
                ]:

                    st.warning(
                        f"📌 {skill}"
                    )


        # ====================================================
        # 16. LEARNING ROADMAP
        # ====================================================

        st.header(
            "📚 Personalized Learning Roadmap"
        )

        st.caption(
            "Recommended learning resources based specifically on your current skill gaps."
        )


        course_df = recommend_courses(
            missing_skills,
            courses_df,
            courses_per_skill=2
        )


        if not course_df.empty:

            st.success(
                f"🎓 {len(course_df)} personalized learning recommendations found!"
            )


            roadmap_columns = st.columns(2)


            for index, (_, course) in enumerate(
                course_df.iterrows(),
                start=1
            ):

                with roadmap_columns[
                    (index - 1) % 2
                ]:

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            f"📚 {course['course']}"
                        )

                        st.markdown(
                            f"**🎯 Skill:** {course['skill']}"
                        )

                        st.caption(
                            f"📍 Platform: {course['platform']}"
                        )

                        st.caption(
                            f"📊 Level: {course['level']}"
                        )

                        st.caption(
                            f"⏱️ Duration: {course['duration']}"
                        )


        else:

            st.success(
                "🎉 No major learning gaps found! "
                "Your current skill profile is already well aligned."
            )


        # ====================================================
        # 17. LEARNING STRATEGY
        # ====================================================

        st.subheader(
            "🗺️ Recommended Learning Strategy"
        )


        if missing_skills:

            st.info(
                "Start with the most important missing skills "
                "for your target role. After learning each major "
                "skill, build a small practical project to turn "
                "knowledge into demonstrable experience."
            )

        else:

            st.success(
                "Your skill profile is already strongly aligned "
                "with your recommended career path. Focus next "
                "on projects, interview preparation and real-world "
                "application."
            )


        # ====================================================
        # 18. RESUME TEXT
        # ====================================================

        with st.expander(
            "📄 View Extracted Resume Text"
        ):

            st.text(
                resume_text
            )


        # ====================================================
        # 19. COMPLETION
        # ====================================================

        st.divider()

        st.success(
            f"""
🎉 **SkillShield Analysis Completed!**

Your strongest career match is **{top_role['job_role']}**
with a **{top_score:.1f}% skill match**.

Your estimated career readiness is **{readiness}%**.

Use your skill-gap analysis and personalized learning
roadmap to strengthen your profile.
"""
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )


    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

        if os.path.exists(
            temp_file
        ):

            os.remove(
                temp_file
            )