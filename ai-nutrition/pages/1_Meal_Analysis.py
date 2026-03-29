import pandas as pd
import streamlit as st

from nutrition_utils import (
    analyze_meal,
    apply_app_theme,
    build_food_dataframe,
    ensure_session_state,
    get_analysis_suggestions,
    get_goal_recommendations,
    get_personalized_target,
    get_profile_summary,
    render_header,
    render_macro_chart,
    render_section_card,
    render_sidebar,
    render_stat_cards,
)


st.set_page_config(page_title="Meal Analysis", page_icon="🍽️", layout="wide")

ensure_session_state()
apply_app_theme()
render_sidebar()
render_header("🍽️ Meal Analysis", "Build a meal, preview nutrition, and get goal-based recommendations.")

food_df = build_food_dataframe()
profile = st.session_state.user_profile
profile_summary = get_profile_summary(profile)

search_term = st.text_input("🔍 Search Food Items", placeholder="Type to filter foods")
filtered_foods = food_df["food"].tolist()
if search_term.strip():
    filtered_foods = food_df[
        food_df["food"].str.contains(search_term.strip(), case=False, na=False)
    ]["food"].tolist()

left, right = st.columns([1.4, 1])

with left:
    food_name = st.multiselect("Select Food Items", filtered_foods)

    quantities = {}
    if food_name:
        st.markdown("### Quantity")
        for food in food_name:
            quantities[food] = st.number_input(
                f"Quantity for {food}",
                min_value=1,
                value=1,
                step=1,
                key=f"qty_{food}",
            )

    goal_options = ["Weight Loss", "Muscle Gain", "Maintain"]
    goal = st.selectbox(
        "Select Your Goal",
        goal_options,
        index=goal_options.index(profile["goal"]),
    )
    meal_type = st.selectbox("Select Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
    target_calories = st.number_input(
        "Customize Daily Calorie Target",
        min_value=1000,
        max_value=5000,
        value=get_personalized_target({**profile, "goal": goal}),
        step=50,
    )

with right:
    render_section_card(
        "Profile-Based Target",
        f"""
        <p><strong>BMI:</strong> {profile_summary['bmi']:.1f} ({profile_summary['bmi_category']})</p>
        <p><strong>Estimated TDEE:</strong> {profile_summary['tdee']} kcal</p>
        <p><strong>Suggested target for {goal}:</strong> {get_personalized_target({**profile, 'goal': goal})} kcal</p>
        """,
        pills=[profile["activity_level"], profile["goal"]],
    )
    st.markdown("### Suggested Foods For Your Goal")
    st.dataframe(
        get_goal_recommendations(food_df, goal),
        use_container_width=True,
        hide_index=True,
    )

if food_name:
    render_section_card(
        "Selected Food Preview",
        "<p>Check totals before you analyze so you can tune the meal quantity and balance.</p>",
        pills=[meal_type, goal],
    )
    preview_rows = []
    for food in food_name:
        selected_food = food_df[food_df["food"] == food].iloc[0]
        qty = quantities[food]
        preview_rows.append(
            {
                "Food": food,
                "Qty": qty,
                "Calories": selected_food["calories"] * qty,
                "Protein": selected_food["protein"] * qty,
                "Carbs": selected_food["carbs"] * qty,
                "Fat": selected_food["fat"] * qty,
            }
        )

    preview_df = pd.DataFrame(preview_rows)
    st.dataframe(preview_df, use_container_width=True, hide_index=True)
    st.caption(
        f"Estimated totals: {preview_df['Calories'].sum()} kcal | "
        f"Protein {preview_df['Protein'].sum()} g | "
        f"Carbs {preview_df['Carbs'].sum()} g | "
        f"Fat {preview_df['Fat'].sum()} g"
    )

if st.button("Analyze Meal", type="primary"):
    if not food_name:
        st.warning("Please select at least one food item.")
        st.session_state.last_analysis = None
    else:
        st.session_state.last_analysis = analyze_meal(
            food_df=food_df,
            foods=food_name,
            quantities=quantities,
            goal=goal,
            meal_type=meal_type,
            target_calories=target_calories,
        )

analysis = st.session_state.last_analysis

if analysis is not None:
    st.markdown("---")
    render_section_card(
        "Nutrition Result",
        f"<p>Foods: {', '.join(analysis['foods'])}</p><p>Goal: {analysis['goal']} | Meal Type: {analysis['meal_type']}</p>",
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

    st.progress(analysis["health_score"] / 100)
    st.write(f"Health Score: {analysis['health_score']}/100")

    st.markdown("### Macro Breakdown")
    render_macro_chart(
        [analysis["protein"], analysis["carbs"], analysis["fat"]],
        "Meal Macronutrient Distribution",
    )

    st.markdown("### Recommendation")
    if analysis["goal"] == "Weight Loss":
        if analysis["calories"] > 300:
            st.warning("This meal is a bit high in calories for weight loss. Consider reducing quantity or choosing a lighter food.")
        else:
            st.success("Good choice for weight loss. This food is relatively moderate in calories.")
    elif analysis["goal"] == "Muscle Gain":
        if analysis["protein"] >= 15:
            st.success("Good choice for muscle gain. This food provides a decent amount of protein.")
        else:
            st.warning("Protein is a bit low for muscle gain. Consider adding eggs, chicken breast, paneer, or curd.")
    else:
        st.info("This looks fine for a balanced diet. Try to maintain variety across protein, carbs, and fats.")

    st.markdown("### Next Meal Suggestion")
    for suggestion in get_analysis_suggestions(analysis):
        st.info(suggestion)

    if st.button("➕ Add to Daily Total"):
        st.session_state.daily_total["calories"] += analysis["calories"]
        st.session_state.daily_total["protein"] += analysis["protein"]
        st.session_state.daily_total["carbs"] += analysis["carbs"]
        st.session_state.daily_total["fat"] += analysis["fat"]
        st.session_state.meal_log.append(
            {
                "meal": analysis["meal_type"],
                "foods": ", ".join(analysis["foods"]),
                "calories": analysis["calories"],
                "protein": analysis["protein"],
                "carbs": analysis["carbs"],
                "fat": analysis["fat"],
                "goal": analysis["goal"],
            }
        )
        st.session_state.added_message = "Added to daily total!"
        st.rerun()
