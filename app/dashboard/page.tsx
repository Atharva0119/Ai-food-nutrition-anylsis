"use client";

import { Card, Hero, ProgressBar, StatGrid } from "@/components/ui";
import { useAppState } from "@/lib/app-state";
import { getDailyWarnings, getPersonalizedTarget, getProfileSummary } from "@/lib/nutrition";

export default function DashboardPage() {
  const { dailyTotal, mealLog, resetDailyTotal, userProfile } = useAppState();
  const profile = getProfileSummary(userProfile);
  const targetCalories = getPersonalizedTarget(userProfile);
  const progress = targetCalories ? (dailyTotal.calories / targetCalories) * 100 : 0;
  const warnings = getDailyWarnings(dailyTotal, targetCalories);

  const csv = [
    "meal,foods,calories,protein,carbs,fat,goal",
    ...mealLog.map((entry) =>
      [entry.meal, `"${entry.foods}"`, entry.calories, entry.protein, entry.carbs, entry.fat, entry.goal].join(",")
    )
  ].join("\n");

  return (
    <div className="page-stack">
      <Hero
        title="Daily Dashboard"
        subtitle="Track your totals, monitor goal progress, and export your meal log."
        pills={[`Target ${targetCalories} kcal`, `${userProfile.goal}`, userProfile.activity_level]}
      />

      <Card title="Profile Context">
        <StatGrid
          items={[
            { label: "BMI", value: `${profile.bmi.toFixed(1)} (${profile.bmiCategory})` },
            { label: "TDEE", value: `${profile.tdee} kcal` },
            { label: "Goal", value: userProfile.goal },
            { label: "Remaining", value: `${targetCalories - dailyTotal.calories} kcal` }
          ]}
        />
      </Card>

      <StatGrid
        items={[
          { label: "Calories", value: `${dailyTotal.calories} kcal` },
          { label: "Protein", value: `${dailyTotal.protein} g` },
          { label: "Carbs", value: `${dailyTotal.carbs} g` },
          { label: "Fat", value: `${dailyTotal.fat} g` }
        ]}
      />

      <Card title="Goal Progress">
        <div className="muted" style={{ marginBottom: "0.45rem" }}>
          {progress.toFixed(1)}% of your daily goal
        </div>
        <ProgressBar value={progress} />
      </Card>

      <div className="two-grid">
        <Card title="Smart Daily Insights">
          <div className="list">
            {warnings.map((warning) => (
              <div className="list-item" key={warning}>
                {warning}
              </div>
            ))}
          </div>
        </Card>

        <Card title="Daily Macro Distribution">
          <div className="chart-bars">
            {[
              { label: "Protein", value: dailyTotal.protein },
              { label: "Carbs", value: dailyTotal.carbs },
              { label: "Fat", value: dailyTotal.fat }
            ].map((item) => {
              const total = dailyTotal.protein + dailyTotal.carbs + dailyTotal.fat || 1;
              return (
                <div className="bar-row" key={item.label}>
                  <span>{item.label}</span>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${(item.value / total) * 100}%` }} />
                  </div>
                  <span>{item.value} g</span>
                </div>
              );
            })}
          </div>
        </Card>
      </div>

      <Card
        title="Daily Meal Log"
        actions={
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap" }}>
            <a
              className="button secondary"
              href={`data:text/csv;charset=utf-8,${encodeURIComponent(csv)}`}
              download="daily_meal_log.csv"
            >
              Download Meal Log
            </a>
            <button className="button" onClick={resetDailyTotal}>
              Reset Daily Total
            </button>
          </div>
        }
      >
        {mealLog.length ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Meal</th>
                  <th>Foods</th>
                  <th>Calories</th>
                  <th>Protein</th>
                  <th>Carbs</th>
                  <th>Fat</th>
                  <th>Goal</th>
                </tr>
              </thead>
              <tbody>
                {mealLog.map((entry, index) => (
                  <tr key={`${entry.meal}-${index}`}>
                    <td>{entry.meal}</td>
                    <td>{entry.foods}</td>
                    <td>{entry.calories}</td>
                    <td>{entry.protein}</td>
                    <td>{entry.carbs}</td>
                    <td>{entry.fat}</td>
                    <td>{entry.goal}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty">No meals added yet. Analyze a meal and add it to the daily total first.</div>
        )}
      </Card>
    </div>
  );
}
