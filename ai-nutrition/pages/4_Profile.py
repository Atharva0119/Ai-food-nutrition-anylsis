import streamlit as st

from nutrition_utils import (
    ACTIVITY_MULTIPLIERS,
    apply_app_theme,
    ensure_session_state,
    get_profile_summary,
    render_header,
    render_section_card,
    render_sidebar,
    render_stat_cards,
)


st.set_page_config(page_title="Profile", page_icon="🧍", layout="wide")

ensure_session_state()
apply_app_theme()
render_sidebar()
render_header("🧍 Profile", "Set your body stats and activity level to get smarter calorie targets.")

profile = st.session_state.user_profile.copy()

with st.form("profile_form"):
    col1, col2, col3 = st.columns(3)
    age = col1.number_input("Age", min_value=10, max_value=100, value=int(profile["age"]), step=1)
    weight = col2.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=float(profile["weight"]), step=0.5)
    height = col3.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=float(profile["height"]), step=0.5)

    col4, col5, col6 = st.columns(3)
    gender = col4.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(profile["gender"]))
    activity_level = col5.selectbox(
        "Activity Level",
        list(ACTIVITY_MULTIPLIERS.keys()),
        index=list(ACTIVITY_MULTIPLIERS.keys()).index(profile["activity_level"]),
    )
    goal_options = ["Weight Loss", "Muscle Gain", "Maintain"]
    goal = col6.selectbox("Primary Goal", goal_options, index=goal_options.index(profile["goal"]))

    submitted = st.form_submit_button("Save Profile", type="primary")

if submitted:
    st.session_state.user_profile = {
        "age": int(age),
        "weight": float(weight),
        "height": float(height),
        "gender": gender,
        "activity_level": activity_level,
        "goal": goal,
    }
    profile = st.session_state.user_profile.copy()
    st.success("Profile updated successfully.")

summary = get_profile_summary(profile)

render_stat_cards(
    [
        {"label": "BMI", "value": f"{summary['bmi']:.1f}"},
        {"label": "BMI Category", "value": summary["bmi_category"]},
        {"label": "BMR", "value": f"{summary['bmr']} kcal"},
        {"label": "TDEE", "value": f"{summary['tdee']} kcal"},
    ]
)

render_section_card(
    "Personalized Daily Plan",
    f"""
    <p><strong>Suggested Calorie Target:</strong> {summary['target_calories']} kcal</p>
    <p><strong>Goal:</strong> {profile['goal']}</p>
    <p><strong>Activity level:</strong> {profile['activity_level']}</p>
    <p><strong>Height:</strong> {profile['height']} cm | <strong>Weight:</strong> {profile['weight']} kg</p>
    """,
    pills=["Profile-driven targets", "Adaptive dashboard"],
)

st.info(
    "Your profile now drives the suggested calorie target on the Meal Analysis and Daily Dashboard pages."
)
