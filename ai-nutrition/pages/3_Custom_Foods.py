import streamlit as st

import pandas as pd

from nutrition_utils import (
    apply_app_theme,
    build_food_dataframe,
    ensure_session_state,
    render_header,
    render_section_card,
    render_sidebar,
    render_stat_cards,
)


st.set_page_config(page_title="Custom Foods", page_icon="🧾", layout="wide")

ensure_session_state()
apply_app_theme()
render_sidebar()
render_header("🧾 Custom Foods", "Add your own food items and review the full food list.")

food_df = build_food_dataframe()

render_stat_cards(
    [
        {"label": "Custom Foods", "value": len(st.session_state.custom_foods), "help": "Foods you created"},
        {"label": "Total Foods", "value": len(food_df), "help": "Database size"},
    ]
)

render_section_card(
    "Food Studio",
    "<p>Add missing ingredients or your own meal staples so analysis stays personal and flexible.</p>",
    pills=["Custom database", "Reusable entries"],
)

with st.form("custom_food_form", clear_on_submit=True):
    c1, c2, c3, c4, c5 = st.columns(5)
    custom_food_name = c1.text_input("Food name")
    custom_calories = c2.number_input("Calories", min_value=0, value=100, step=1)
    custom_protein = c3.number_input("Protein (g)", min_value=0, value=5, step=1)
    custom_carbs = c4.number_input("Carbs (g)", min_value=0, value=10, step=1)
    custom_fat = c5.number_input("Fat (g)", min_value=0, value=3, step=1)
    add_custom_food = st.form_submit_button("Add Food", type="primary")

if add_custom_food:
    normalized_name = custom_food_name.strip().lower()
    existing_names = set(food_df["food"].str.lower())

    if not normalized_name:
        st.warning("Please enter a food name.")
    elif normalized_name in existing_names:
        st.warning("That food already exists in the list.")
    else:
        st.session_state.custom_foods.append(
            {
                "food": custom_food_name.strip(),
                "calories": custom_calories,
                "protein": custom_protein,
                "carbs": custom_carbs,
                "fat": custom_fat,
            }
        )
        st.success(f"{custom_food_name.strip()} added successfully.")
        st.rerun()

st.markdown("### Your Custom Foods")
if st.session_state.custom_foods:
    custom_foods_df = pd.DataFrame(st.session_state.custom_foods)
    st.dataframe(custom_foods_df, use_container_width=True, hide_index=True)
else:
    st.info("You have not added any custom foods yet.")

st.markdown("### Full Food Database")
search_term = st.text_input("Search all foods", placeholder="Type a food name")
display_df = food_df.copy()
if search_term.strip():
    display_df = display_df[
        display_df["food"].str.contains(search_term.strip(), case=False, na=False)
    ]

st.dataframe(display_df, use_container_width=True, hide_index=True)
