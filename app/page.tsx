"use client";

import { Card, Hero, StatGrid } from "@/components/ui";
import { useAppState } from "@/lib/app-state";
import { getFoodData, getProfileSummary } from "@/lib/nutrition";

export default function HomePage() {
  const { customFoods, dailyTotal, lastAnalysis, mealLog, userProfile } = useAppState();
  const foodData = getFoodData(customFoods);
  const profile = getProfileSummary(userProfile);

  return (
    <div className="page-stack">
      <Hero
        title="AI Nutrition Assistant"
        subtitle="A Vercel-ready rebuild of your nutrition app with profile-driven calorie targets, meal scoring, custom foods, and daily tracking."
        pills={["Vercel ready", "Dark mode friendly", "Local persistence"]}
      />

      <div className="layout-grid">
        <Card title="Product Overview">
          <p className="muted">
            Move through the app in the same flow you already had: update your profile, analyze meals, save them to your day,
            and manage your food database.
          </p>
          <div className="pill-row">
            <span className="pill">Profile-based targets</span>
            <span className="pill">Meal recommendations</span>
            <span className="pill">Custom food library</span>
            <span className="pill">Daily dashboard</span>
          </div>
        </Card>

        <Card title="Profile Snapshot">
          <StatGrid
            items={[
              { label: "Goal", value: userProfile.goal },
              { label: "Activity", value: userProfile.activity_level },
              { label: "BMI", value: `${profile.bmi.toFixed(1)} (${profile.bmiCategory})` },
              { label: "Suggested Calories", value: `${profile.targetCalories} kcal` }
            ]}
          />
        </Card>
      </div>

      <StatGrid
        items={[
          { label: "Foods Available", value: foodData.length, help: "Base + custom foods" },
          { label: "Custom Foods", value: customFoods.length, help: "Added by you" },
          { label: "Meals Logged", value: mealLog.length, help: "Tracked today" },
          { label: "Calories Today", value: `${dailyTotal.calories} kcal`, help: "Current running total" }
        ]}
      />

      {lastAnalysis ? (
        <Card title="Latest Meal Analysis">
          <p className="muted">
            Last analyzed foods: {lastAnalysis.foods.join(", ")} | Goal: {lastAnalysis.goal} | Meal: {lastAnalysis.meal_type}
          </p>
          <StatGrid
            items={[
              { label: "Calories", value: `${lastAnalysis.calories} kcal` },
              { label: "Protein", value: `${lastAnalysis.protein} g` },
              { label: "Carbs", value: `${lastAnalysis.carbs} g` },
              { label: "Fat", value: `${lastAnalysis.fat} g` }
            ]}
          />
        </Card>
      ) : (
        <div className="empty">No meal analysis yet. Open Meal Analysis to get started.</div>
      )}
    </div>
  );
}
