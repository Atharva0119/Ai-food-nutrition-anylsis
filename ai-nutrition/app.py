import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Nutrition Assistant", page_icon="🥗", layout="centered")

st.sidebar.title("🥗 AI Nutrition Assistant")
st.sidebar.write("Analyze your meals and get smart recommendations.")
st.sidebar.markdown("### Instructions")
st.sidebar.write("""
1. Select food item(s)
2. Enter quantity for each selected food
3. Select your goal
4. Select meal type
5. Click Analyze
6. Add meal to daily total
""")

# Load food dataset
df = pd.read_csv("food_data.csv")

# Session state setup
if "daily_total" not in st.session_state:
    st.session_state.daily_total = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "meal_log" not in st.session_state:
    st.session_state.meal_log = []

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #16a34a, #22c55e);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 20px;'>
    <h1 style='margin:0;'>🥗 AI-Based Food Nutrition Analysis</h1>
    <p style='margin:8px 0 0 0; font-size:18px;'>
        Analyze your meal and get goal-based smart recommendations
    </p>
</div>
""", unsafe_allow_html=True)

st.subheader("🍽️ Enter Your Meal Details")

# Daily tracker
st.markdown("### 📅 Daily Nutrition Tracker")
tracker = st.session_state.daily_total

if "added_message" in st.session_state:
    st.success(st.session_state.added_message)
    del st.session_state["added_message"]

t1, t2, t3, t4 = st.columns(4)
t1.metric("Daily Calories", f"{tracker['calories']} kcal")
t2.metric("Daily Protein", f"{tracker['protein']} g")
t3.metric("Daily Carbs", f"{tracker['carbs']} g")
t4.metric("Daily Fat", f"{tracker['fat']} g")

st.markdown("### 📝 Daily Meal Log")
if st.session_state.meal_log:
    for entry in st.session_state.meal_log:
        st.write(
            f"**{entry['meal']}** → {entry['foods']} | "
            f"{entry['calories']} kcal | Protein: {entry['protein']} g"
        )
else:
    st.write("No meals added yet.")

if st.button("🔄 Reset Daily Total"):
    st.session_state.daily_total = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }
    st.session_state.meal_log = []
    st.session_state.last_analysis = None
    st.session_state.added_message = "Daily total and meal log reset successfully."
    st.rerun()

st.markdown("---")

# Inputs
food_name = st.multiselect("Select Food Items", df["food"].tolist())

quantities = {}
if food_name:
    st.markdown("### 🔢 Enter Quantity for Each Food")
    for food in food_name:
        quantities[food] = st.number_input(
            f"Quantity for {food}",
            min_value=1,
            value=1,
            step=1,
            key=f"qty_{food}"
        )

goal = st.selectbox("Select Your Goal", ["Weight Loss", "Muscle Gain", "Maintain"])
meal_type = st.selectbox("Select Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])

# Goal-based target calories
if goal == "Weight Loss":
    target_calories = 1800
elif goal == "Muscle Gain":
    target_calories = 2500
else:
    target_calories = 2200

remaining_calories = target_calories - tracker["calories"]

st.markdown("### 🎯 Daily Goal Summary")

progress = (tracker["calories"] / target_calories) * 100 if target_calories > 0 else 0

g1, g2, g3 = st.columns(3)
g1.metric("Target Calories", f"{target_calories} kcal")
g2.metric("Consumed", f"{tracker['calories']} kcal")
g3.metric("Remaining", f"{remaining_calories} kcal")

st.progress(min(progress / 100, 1.0))
st.write(f"Progress: {progress:.1f}% of daily goal")

st.markdown("### ⚠️ Smart Daily Insights")

warnings = []

if tracker["calories"] > target_calories:
    warnings.append("You have exceeded your daily calorie target.")
elif tracker["calories"] > 0.8 * target_calories:
    warnings.append("You are close to your daily calorie limit.")

if tracker["protein"] < 40:
    warnings.append("Protein intake is low today. Consider adding protein-rich foods.")

if tracker["carbs"] > 200:
    warnings.append("Carbohydrate intake is relatively high today.")

if not warnings:
    warnings.append("Great job! Your daily intake is balanced so far.")

for w in warnings:
    st.warning(w)

st.markdown("---")

# Analyze action
if st.button("Analyze"):
    if not food_name:
        st.warning("Please select at least one food item.")
        st.session_state.last_analysis = None
    else:
        calories = 0
        protein = 0
        carbs = 0
        fat = 0

        for food in food_name:
            selected_food = df[df["food"] == food].iloc[0]
            qty = quantities[food]

            calories += selected_food["calories"] * qty
            protein += selected_food["protein"] * qty
            carbs += selected_food["carbs"] * qty
            fat += selected_food["fat"] * qty

        health_score = 0

        if goal == "Weight Loss":
            if calories <= 300:
                health_score += 50
            if protein >= 5:
                health_score += 30
            if carbs < 50:
                health_score += 20

        elif goal == "Muscle Gain":
            if protein >= 15:
                health_score += 50
            if calories >= 300:
                health_score += 30
            if fat < 20:
                health_score += 20

        elif goal == "Maintain":
            if calories < 500:
                health_score += 50
            if protein >= 5:
                health_score += 25
            if carbs < 60:
                health_score += 25

        st.session_state.last_analysis = {
            "foods": food_name,
            "quantities": quantities.copy(),
            "goal": goal,
            "meal_type": meal_type,
            "target_calories": target_calories,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "health_score": health_score
        }

analysis = st.session_state.last_analysis

if analysis is not None:
    st.markdown("---")
    st.subheader("Nutrition Result")

    st.subheader("📊 Health Score")
    st.progress(analysis["health_score"] / 100)
    st.write(f"Score: {analysis['health_score']}/100")

    st.write(f"**Foods Selected:** {', '.join(analysis['foods'])}")

    st.markdown("**Selected Quantities:**")
    for food, qty in analysis["quantities"].items():
        st.write(f"- {food}: {qty}")

    st.write(f"**Goal:** {analysis['goal']}")
    st.write(f"**Meal Type:** {analysis['meal_type']}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Calories", f"{analysis['calories']} kcal")
    col2.metric("Protein", f"{analysis['protein']} g")
    col3.metric("Carbs", f"{analysis['carbs']} g")
    col4.metric("Fat", f"{analysis['fat']} g")

    st.subheader("📈 Nutrition Breakdown")
    labels = ["Protein", "Carbs", "Fat"]
    values = [analysis["protein"], analysis["carbs"], analysis["fat"]]

    if sum(values) > 0:
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Macronutrient Distribution")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Chart cannot be displayed because nutrition values are zero.")

    st.subheader("AI Recommendation")

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

    elif analysis["goal"] == "Maintain":
        st.info("This looks fine for a balanced diet. Try to maintain variety across protein, carbs, and fats.")

    st.subheader("Final Decision")

    if analysis["goal"] == "Weight Loss":
        if analysis["calories"] <= 300 and analysis["protein"] >= 5:
            st.success("Agent Decision: Suitable choice for weight loss.")
        elif analysis["calories"] > 300:
            st.error("Agent Decision: Not the best choice for weight loss in this quantity.")
        else:
            st.warning("Agent Decision: Acceptable, but could be improved with more protein.")

    elif analysis["goal"] == "Muscle Gain":
        if analysis["protein"] >= 15:
            st.success("Agent Decision: Strong choice for muscle gain.")
        else:
            st.warning("Agent Decision: This meal needs more protein for muscle gain.")

    elif analysis["goal"] == "Maintain":
        if analysis["calories"] < 500:
            st.success("Agent Decision: Balanced enough for maintenance.")
        else:
            st.warning("Agent Decision: Fine occasionally, but watch portion size for maintenance.")

    st.subheader("🍽️ Next Meal Suggestion")

    suggestions = []

    if analysis["protein"] < 15:
        suggestions.append("Increase protein intake: add eggs, paneer, chicken breast, or curd.")

    if analysis["carbs"] > 60:
        suggestions.append("Carbs are high: next meal should be lighter, such as salad, fruits, or protein-rich food.")

    if analysis["calories"] > 400:
        suggestions.append("High calorie intake: keep next meal low calorie.")

    if analysis["goal"] == "Muscle Gain" and analysis["protein"] < 20:
        suggestions.append("For muscle gain, focus on high-protein foods in the next meal.")

    if analysis["goal"] == "Weight Loss" and analysis["calories"] > 300:
        suggestions.append("For weight loss, next meal should be low-calorie and high in fiber.")

    if not suggestions:
        suggestions.append("Great balance! Maintain similar food choices for the next meal.")

    for s in suggestions:
        st.info(s)

    if st.button("➕ Add to Daily Total"):
        st.session_state.daily_total["calories"] += analysis["calories"]
        st.session_state.daily_total["protein"] += analysis["protein"]
        st.session_state.daily_total["carbs"] += analysis["carbs"]
        st.session_state.daily_total["fat"] += analysis["fat"]

        st.session_state.meal_log.append({
            "meal": analysis["meal_type"],
            "foods": ", ".join(analysis["foods"]),
            "calories": analysis["calories"],
            "protein": analysis["protein"]
        })

        st.session_state.added_message = "Added to daily total!"
        st.rerun()