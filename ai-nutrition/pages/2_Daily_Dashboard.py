import pandas as pd
import streamlit as st

from nutrition_utils import (
    apply_app_theme,
    ensure_session_state,
    get_daily_warnings,
    get_personalized_target,
    get_profile_summary,
    render_header,
    render_macro_chart,
    render_section_card,
    render_sidebar,
    render_stat_cards,
    reset_daily_total,
)


st.set_page_config(page_title="Daily Dashboard", page_icon="📊", layout="wide")

ensure_session_state()
apply_app_theme()
render_sidebar()
render_header("📊 Daily Dashboard", "Track totals, review smart insights, and export your meal log.")

tracker = st.session_state.daily_total
profile = st.session_state.user_profile
profile_summary = get_profile_summary(profile)

if st.session_state.added_message:
    st.success(st.session_state.added_message)
    st.session_state.added_message = None

goal_options = ["Weight Loss", "Muscle Gain", "Maintain"]
goal = st.selectbox("Daily Goal Mode", goal_options, index=goal_options.index(profile["goal"]))
target_calories = st.number_input(
    "Daily Calorie Target",
    min_value=1000,
    max_value=5000,
    value=get_personalized_target({**profile, "goal": goal}),
    step=50,
)

render_section_card(
    "Profile Context",
    f"""
    <p><strong>BMI:</strong> {profile_summary['bmi']:.1f} ({profile_summary['bmi_category']})</p>
    <p><strong>TDEE:</strong> {profile_summary['tdee']} kcal</p>
    <p><strong>Goal mode:</strong> {goal}</p>
    """,
    pills=[profile["activity_level"], f"Target {target_calories} kcal"],
)

render_stat_cards(
    [
        {"label": "Calories", "value": f"{tracker['calories']} kcal"},
        {"label": "Protein", "value": f"{tracker['protein']} g"},
        {"label": "Carbs", "value": f"{tracker['carbs']} g"},
        {"label": "Fat", "value": f"{tracker['fat']} g"},
    ]
)

remaining_calories = target_calories - tracker["calories"]
progress = (tracker["calories"] / target_calories) * 100 if target_calories > 0 else 0

st.markdown("### Goal Summary")
g1, g2, g3 = st.columns(3)
g1.metric("Target", f"{target_calories} kcal")
g2.metric("Consumed", f"{tracker['calories']} kcal")
g3.metric("Remaining", f"{remaining_calories} kcal")
st.progress(min(progress / 100, 1.0))
st.write(f"Progress: {progress:.1f}% of daily goal")

st.markdown("### Smart Daily Insights")
for warning in get_daily_warnings(tracker, target_calories):
    st.warning(warning)

st.markdown("### Daily Macro Distribution")
render_macro_chart(
    [tracker["protein"], tracker["carbs"], tracker["fat"]],
    "Today's Macro Split",
)

st.markdown("### Daily Meal Log")
if st.session_state.meal_log:
    meal_log_df = pd.DataFrame(st.session_state.meal_log)
    st.dataframe(meal_log_df, use_container_width=True, hide_index=True)
    st.download_button(
        label="⬇️ Download Meal Log",
        data=meal_log_df.to_csv(index=False).encode("utf-8"),
        file_name="daily_meal_log.csv",
        mime="text/csv",
    )
else:
    st.info("No meals added yet. Analyze a meal and add it to the daily total first.")

if st.button("🔄 Reset Daily Total"):
    reset_daily_total()
    st.rerun()
