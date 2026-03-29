import streamlit as st

from nutrition_utils import (
    apply_app_theme,
    build_food_dataframe,
    ensure_session_state,
    get_profile_summary,
    render_header,
    render_section_card,
    render_sidebar,
    render_stat_cards,
)


st.set_page_config(page_title="AI Nutrition Assistant", page_icon="🥗", layout="wide")

ensure_session_state()
apply_app_theme()
render_sidebar()
render_header(
    "🥗 AI Nutrition Assistant",
    "A multi-page nutrition app for meal analysis, food management, and daily tracking.",
)

food_df = build_food_dataframe()
tracker = st.session_state.daily_total
profile = st.session_state.user_profile
profile_summary = get_profile_summary(profile)

left, right = st.columns([1.2, 1])

with left:
    render_section_card(
        "Welcome",
        """
        <p>Use the page navigation to move through a more complete nutrition workflow.</p>
        <p><strong>Profile</strong> personalizes your targets. <strong>Meal Analysis</strong> scores meals before you log them.
        <strong>Daily Dashboard</strong> tracks progress. <strong>Custom Foods</strong> expands your database.</p>
        """,
        pills=["Profile-based targets", "Meal scoring", "Daily insights", "Custom foods"],
    )

    render_stat_cards(
        [
            {"label": "Foods Available", "value": len(food_df), "help": "Base + custom foods"},
            {"label": "Custom Foods", "value": len(st.session_state.custom_foods), "help": "Added by you"},
            {"label": "Meals Logged", "value": len(st.session_state.meal_log), "help": "Tracked today"},
            {"label": "Calories Today", "value": f"{tracker['calories']} kcal", "help": "Running total"},
        ]
    )

with right:
    render_section_card(
        "Profile Snapshot",
        f"""
        <p><strong>Goal:</strong> {profile['goal']}</p>
        <p><strong>Activity:</strong> {profile['activity_level']}</p>
        <p><strong>BMI:</strong> {profile_summary['bmi']:.1f} ({profile_summary['bmi_category']})</p>
        <p><strong>Suggested Calories:</strong> {profile_summary['target_calories']} kcal</p>
        """,
        pills=["Personalized", "TDEE-backed"],
    )

render_stat_cards(
    [
        {"label": "Protein", "value": f"{tracker['protein']} g"},
        {"label": "Carbs", "value": f"{tracker['carbs']} g"},
        {"label": "Fat", "value": f"{tracker['fat']} g"},
    ]
)

if st.session_state.last_analysis is not None:
    analysis = st.session_state.last_analysis
    st.markdown("---")
    render_section_card(
        "Latest Meal Analysis",
        f"<p>Last analyzed foods: {', '.join(analysis['foods'])}</p><p>Goal: {analysis['goal']} | Meal: {analysis['meal_type']}</p>",
        pills=[f"Health Score {analysis['health_score']}/100"],
    )
    render_stat_cards(
        [
            {"label": "Calories", "value": f"{analysis['calories']} kcal"},
            {"label": "Protein", "value": f"{analysis['protein']} g"},
            {"label": "Carbs", "value": f"{analysis['carbs']} g"},
            {"label": "Fat", "value": f"{analysis['fat']} g"},
        ]
    )
else:
    st.info("No meal analysis yet. Open the `Meal Analysis` page to get started.")
