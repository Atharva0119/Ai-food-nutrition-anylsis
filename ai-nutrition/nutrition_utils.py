from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DAILY_TOTAL = {
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
}
DEFAULT_PROFILE = {
    "age": 25,
    "weight": 70.0,
    "height": 170.0,
    "gender": "Male",
    "activity_level": "Moderately Active",
    "goal": "Maintain",
}
ACTIVITY_MULTIPLIERS = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725,
    "Extra Active": 1.9,
}


def load_base_food_data():
    return pd.read_csv(BASE_DIR / "food_data.csv")


def ensure_session_state():
    if "daily_total" not in st.session_state:
        st.session_state.daily_total = DEFAULT_DAILY_TOTAL.copy()

    if "last_analysis" not in st.session_state:
        st.session_state.last_analysis = None

    if "meal_log" not in st.session_state:
        st.session_state.meal_log = []

    if "custom_foods" not in st.session_state:
        st.session_state.custom_foods = []

    if "added_message" not in st.session_state:
        st.session_state.added_message = None

    if "user_profile" not in st.session_state:
        st.session_state.user_profile = DEFAULT_PROFILE.copy()


def apply_app_theme():
    st.markdown(
        """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=DM+Sans:wght@400;500;700&display=swap');

    :root {
        --bg: #f4f8f2;
        --bg-top: #fbfdf8;
        --panel: rgba(255, 255, 255, 0.82);
        --panel-strong: #ffffff;
        --ink: #133321;
        --muted: #5f7467;
        --line: rgba(19, 51, 33, 0.08);
        --green: #1f8f5f;
        --green-dark: #13553a;
        --lime: #cce86b;
        --gold: #f4b942;
        --shadow: 0 18px 55px rgba(31, 69, 49, 0.10);
        --surface-strong: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(247, 251, 246, 0.96));
        --surface-soft: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(247, 251, 246, 0.95));
        --table-bg: rgba(255,255,255,0.78);
        --input-bg: rgba(255,255,255,0.85);
        --download-bg: linear-gradient(135deg, #ffffff, #eef8ee);
        color-scheme: light;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg: #0f1713;
            --bg-top: #101d17;
            --panel: rgba(18, 28, 23, 0.82);
            --panel-strong: #121c17;
            --ink: #e8f3ec;
            --muted: #a9bcaf;
            --line: rgba(232, 243, 236, 0.10);
            --green: #2db575;
            --green-dark: #d6f3df;
            --lime: #b7dd58;
            --gold: #f4b942;
            --shadow: 0 18px 55px rgba(0, 0, 0, 0.32);
            --surface-strong: linear-gradient(180deg, rgba(22,32,27,0.98), rgba(16,24,20,0.96));
            --surface-soft: linear-gradient(180deg, rgba(20,30,25,0.96), rgba(15,22,19,0.96));
            --table-bg: rgba(18, 28, 23, 0.88);
            --input-bg: rgba(18, 28, 23, 0.92);
            --download-bg: linear-gradient(135deg, #18231d, #203127);
            color-scheme: dark;
        }
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(204, 232, 107, 0.32), transparent 30%),
            radial-gradient(circle at top right, rgba(31, 143, 95, 0.15), transparent 24%),
            linear-gradient(180deg, var(--bg-top) 0%, var(--bg) 100%);
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        font-family: "DM Sans", sans-serif;
        color: var(--ink);
    }

    h1, h2, h3 {
        font-family: "Space Grotesk", sans-serif;
        letter-spacing: -0.03em;
    }

    [data-testid="stHeader"] {
        background: rgba(255, 255, 255, 0);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #153726 0%, #1d4d35 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f4fff7 !important;
    }

    [data-testid="stSidebarNav"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 18px;
        padding: 0.5rem;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 14px;
        margin: 0.15rem 0;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(204, 232, 107, 0.18);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }

    .hero-shell {
        background:
            linear-gradient(135deg, rgba(19, 85, 58, 0.96), rgba(31, 143, 95, 0.90)),
            linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.14);
        box-shadow: var(--shadow);
        border-radius: 28px;
        padding: 2rem 2rem 1.8rem 2rem;
        color: white;
        position: relative;
        overflow: hidden;
        margin-bottom: 1.4rem;
    }

    .hero-shell::after {
        content: "";
        position: absolute;
        inset: auto -10% -35% auto;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(204, 232, 107, 0.50), transparent 70%);
        pointer-events: none;
    }

    .hero-kicker {
        display: inline-block;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: rgba(255,255,255,0.78);
        margin-bottom: 0.75rem;
    }

    .hero-title {
        font-family: "Space Grotesk", sans-serif;
        font-size: clamp(2rem, 4vw, 3.3rem);
        line-height: 1;
        margin: 0;
    }

    .hero-subtitle {
        max-width: 760px;
        margin: 0.8rem 0 0 0;
        color: rgba(255,255,255,0.82);
        font-size: 1.05rem;
    }

    .surface-card {
        background: var(--panel);
        border: 1px solid var(--line);
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow);
        border-radius: 22px;
        padding: 1.15rem 1.15rem 1rem 1.15rem;
        margin-bottom: 1rem;
    }

    .surface-card h3, .surface-card h4, .surface-card p {
        margin-top: 0;
        color: var(--ink);
    }

    .mini-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.9rem;
        margin: 1rem 0 0.3rem;
    }

    .mini-card {
        background: var(--surface-soft);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        min-height: 104px;
    }

    .mini-label {
        color: var(--muted);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.55rem;
    }

    .mini-value {
        font-family: "Space Grotesk", sans-serif;
        font-weight: 700;
        font-size: 1.55rem;
        color: var(--ink);
        line-height: 1.05;
    }

    .mini-help {
        color: var(--muted);
        font-size: 0.9rem;
        margin-top: 0.45rem;
    }

    .section-label {
        font-family: "Space Grotesk", sans-serif;
        font-size: 1.15rem;
        margin: 0 0 0.85rem 0;
        color: var(--ink);
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.8rem;
    }

    .pill {
        background: rgba(204, 232, 107, 0.45);
        color: var(--green-dark);
        border: 1px solid rgba(19, 85, 58, 0.08);
        border-radius: 999px;
        padding: 0.45rem 0.75rem;
        font-size: 0.88rem;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: var(--surface-strong);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        box-shadow: 0 10px 25px rgba(23, 63, 41, 0.06);
    }

    div[data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"], div[data-testid="stMetricDelta"] {
        color: var(--ink);
    }

    div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        background: var(--table-bg);
        border-radius: 18px;
        border: 1px solid var(--line);
        padding: 0.35rem;
    }

    .stButton > button, .stDownloadButton > button, div[data-testid="stFormSubmitButton"] > button {
        border-radius: 999px;
        border: none;
        padding: 0.65rem 1.15rem;
        font-weight: 700;
        box-shadow: 0 12px 25px rgba(31, 143, 95, 0.18);
    }

    .stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, var(--green) 0%, #29b16f 100%);
        color: white;
    }

    .stDownloadButton > button {
        background: var(--download-bg);
        color: var(--green-dark);
        border: 1px solid var(--line);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stNumberInput > div > div,
    .stTextInput > div > div {
        border-radius: 16px !important;
        border: 1px solid var(--line) !important;
        background: var(--input-bg) !important;
        color: var(--ink) !important;
    }

    label, .stMarkdown, .stCaption, p, li, span {
        color: var(--ink);
    }

    .stSelectbox label, .stTextInput label, .stNumberInput label, .stMultiSelect label {
        color: var(--muted) !important;
    }

    input, textarea {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
    }

    input::placeholder, textarea::placeholder {
        color: var(--muted) !important;
        opacity: 1 !important;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #cce86b, #1f8f5f);
    }

    @media (max-width: 768px) {
        .hero-shell {
            padding: 1.5rem 1.25rem;
        }
    }
</style>
""",
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.sidebar.title("🥗 AI Nutrition Assistant")
    st.sidebar.write("Analyze your meals and get smart recommendations.")
    st.sidebar.markdown("### App Pages")
    st.sidebar.write("Use the page navigation above to move between Home, Meal Analysis, Dashboard, and Custom Foods.")
    st.sidebar.markdown("### Quick Steps")
    st.sidebar.write(
        """
1. Add custom foods if needed
2. Analyze a meal
3. Add it to your daily total
4. Review your dashboard
"""
    )


def render_header(title, subtitle):
    st.markdown(
        f"""
<div class="hero-shell">
    <div class="hero-kicker">Nutrition Intelligence</div>
    <h1 class="hero-title">{title}</h1>
    <p class="hero-subtitle">{subtitle}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def render_section_card(title, body, pills=None):
    pill_markup = ""
    if pills:
        pill_markup = '<div class="pill-row">' + "".join(
            f'<span class="pill">{pill}</span>' for pill in pills
        ) + "</div>"

    st.markdown(
        f"""
<div class="surface-card">
    <div class="section-label">{title}</div>
    <div>{body}</div>
    {pill_markup}
</div>
""",
        unsafe_allow_html=True,
    )


def render_stat_cards(items):
    cards = []
    for item in items:
        help_text = f'<div class="mini-help">{item["help"]}</div>' if item.get("help") else ""
        cards.append(
            f"""
<div class="mini-card">
    <div class="mini-label">{item["label"]}</div>
    <div class="mini-value">{item["value"]}</div>
    {help_text}
</div>
"""
        )

    st.markdown(f'<div class="mini-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def build_food_dataframe():
    food_df = load_base_food_data()
    if st.session_state.custom_foods:
        custom_df = pd.DataFrame(st.session_state.custom_foods)
        food_df = pd.concat([food_df, custom_df], ignore_index=True)
    return food_df


def get_default_target(goal):
    if goal == "Weight Loss":
        return 1800
    if goal == "Muscle Gain":
        return 2500
    return 2200


def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    if height_m <= 0:
        return 0.0
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmr(profile):
    weight = profile["weight"]
    height = profile["height"]
    age = profile["age"]

    if profile["gender"] == "Male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_tdee(profile):
    bmr = calculate_bmr(profile)
    multiplier = ACTIVITY_MULTIPLIERS.get(profile["activity_level"], 1.55)
    return bmr * multiplier


def get_personalized_target(profile):
    tdee = calculate_tdee(profile)
    goal = profile["goal"]

    if goal == "Weight Loss":
        return max(1200, round(tdee - 400))
    if goal == "Muscle Gain":
        return round(tdee + 300)
    return round(tdee)


def get_profile_summary(profile):
    bmi = calculate_bmi(profile["weight"], profile["height"])
    tdee = calculate_tdee(profile)
    target = get_personalized_target(profile)
    return {
        "bmi": bmi,
        "bmi_category": get_bmi_category(bmi),
        "bmr": round(calculate_bmr(profile)),
        "tdee": round(tdee),
        "target_calories": target,
    }


def get_goal_recommendations(food_df, selected_goal):
    recommendations = food_df.copy()
    recommendations["protein_density"] = recommendations["protein"] / recommendations["calories"].clip(lower=1)

    if selected_goal == "Weight Loss":
        recommendations = recommendations.sort_values(
            by=["calories", "protein_density"],
            ascending=[True, False],
        )
    elif selected_goal == "Muscle Gain":
        recommendations = recommendations.sort_values(
            by=["protein", "calories"],
            ascending=[False, False],
        )
    else:
        recommendations = recommendations.sort_values(
            by=["protein_density", "calories"],
            ascending=[False, True],
        )

    return recommendations.head(5)[["food", "calories", "protein", "carbs", "fat"]]


def analyze_meal(food_df, foods, quantities, goal, meal_type, target_calories):
    calories = 0
    protein = 0
    carbs = 0
    fat = 0

    for food in foods:
        selected_food = food_df[food_df["food"] == food].iloc[0]
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
    else:
        if calories < 500:
            health_score += 50
        if protein >= 5:
            health_score += 25
        if carbs < 60:
            health_score += 25

    return {
        "foods": foods,
        "quantities": quantities.copy(),
        "goal": goal,
        "meal_type": meal_type,
        "target_calories": target_calories,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat,
        "health_score": health_score,
    }


def get_analysis_suggestions(analysis):
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

    return suggestions


def get_daily_warnings(tracker, target_calories):
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

    return warnings


def render_macro_chart(values, title):
    if sum(values) <= 0:
        st.info("Chart cannot be displayed because nutrition values are zero.")
        return

    fig, ax = plt.subplots()
    ax.pie(values, labels=["Protein", "Carbs", "Fat"], autopct="%1.1f%%", startangle=90)
    ax.set_title(title)
    st.pyplot(fig)
    plt.close(fig)


def reset_daily_total():
    st.session_state.daily_total = DEFAULT_DAILY_TOTAL.copy()
    st.session_state.meal_log = []
    st.session_state.last_analysis = None
    st.session_state.added_message = "Daily total and meal log reset successfully."
