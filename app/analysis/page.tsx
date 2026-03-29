"use client";

import { useMemo, useState } from "react";

import { Card, Hero, ProgressBar, StatGrid } from "@/components/ui";
import { useAppState } from "@/lib/app-state";
import {
  GOALS,
  MEAL_TYPES,
  analyzeMeal,
  getAnalysisSuggestions,
  getFoodData,
  getGoalRecommendations,
  getPersonalizedTarget,
  getProfileSummary
} from "@/lib/nutrition";

export default function AnalysisPage() {
  const {
    addMealLogEntry,
    customFoods,
    dailyTotal,
    setDailyTotal,
    setLastAnalysis,
    lastAnalysis,
    userProfile
  } = useAppState();

  const foodData = useMemo(() => getFoodData(customFoods), [customFoods]);
  const profileSummary = getProfileSummary(userProfile);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedFoods, setSelectedFoods] = useState<string[]>([]);
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [goal, setGoal] = useState(userProfile.goal);
  const [mealType, setMealType] = useState<(typeof MEAL_TYPES)[number]>("Breakfast");
  const [targetCalories, setTargetCalories] = useState(getPersonalizedTarget(userProfile));

  const filteredFoods = foodData.filter((item) => item.food.toLowerCase().includes(searchTerm.toLowerCase()));
  const recommendations = getGoalRecommendations(foodData, goal);
  const previewRows = selectedFoods.map((name) => {
    const item = foodData.find((food) => food.food === name)!;
    const qty = quantities[name] ?? 1;
    return {
      food: name,
      qty,
      calories: item.calories * qty,
      protein: item.protein * qty,
      carbs: item.carbs * qty,
      fat: item.fat * qty
    };
  });

  const handleAnalyze = () => {
    if (!selectedFoods.length) return;
    const result = analyzeMeal(foodData, selectedFoods, quantities, goal, mealType, targetCalories);
    setLastAnalysis(result);
  };

  const analysis = lastAnalysis;

  return (
    <div className="page-stack">
      <Hero
        title="Meal Analysis"
        subtitle="Build a meal, preview nutrition, and score it against your current goal."
        pills={["Preview totals", "Goal scoring", "Next meal suggestions"]}
      />

      <div className="layout-grid">
        <Card title="Meal Builder">
          <div className="form-grid">
            <div className="field" style={{ gridColumn: "1 / -1" }}>
              <label>Search Food Items</label>
              <input placeholder="Type to filter foods" value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
            </div>

            <div className="field" style={{ gridColumn: "1 / -1" }}>
              <label>Select Food Items</label>
              <select
                multiple
                value={selectedFoods}
                onChange={(e) =>
                  setSelectedFoods(Array.from(e.target.selectedOptions, (option) => option.value))
                }
                style={{ minHeight: 180 }}
              >
                {filteredFoods.map((item) => (
                  <option key={item.food} value={item.food}>
                    {item.food}
                  </option>
                ))}
              </select>
            </div>

            {selectedFoods.map((food) => (
              <div className="field" key={food}>
                <label>Quantity for {food}</label>
                <input
                  type="number"
                  min={1}
                  value={quantities[food] ?? 1}
                  onChange={(e) => setQuantities({ ...quantities, [food]: Number(e.target.value) })}
                />
              </div>
            ))}

            <div className="field">
              <label>Goal</label>
              <select
                value={goal}
                onChange={(e) => {
                  const nextGoal = e.target.value as typeof goal;
                  setGoal(nextGoal);
                  setTargetCalories(getPersonalizedTarget({ ...userProfile, goal: nextGoal }));
                }}
              >
                {GOALS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label>Meal Type</label>
              <select value={mealType} onChange={(e) => setMealType(e.target.value as typeof mealType)}>
                {MEAL_TYPES.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </div>

            <div className="field">
              <label>Daily Calorie Target</label>
              <input type="number" value={targetCalories} onChange={(e) => setTargetCalories(Number(e.target.value))} />
            </div>
          </div>

          <div style={{ marginTop: "1rem" }}>
            <button className="button" onClick={handleAnalyze} disabled={!selectedFoods.length}>
              Analyze Meal
            </button>
          </div>
        </Card>

        <Card title="Profile-Based Target">
          <StatGrid
            items={[
              { label: "BMI", value: `${profileSummary.bmi.toFixed(1)} (${profileSummary.bmiCategory})` },
              { label: "Estimated TDEE", value: `${profileSummary.tdee} kcal` },
              { label: `Suggested Target for ${goal}`, value: `${getPersonalizedTarget({ ...userProfile, goal })} kcal` }
            ]}
          />
        </Card>
      </div>

      <div className="two-grid">
        <Card title="Selected Food Preview">
          {previewRows.length ? (
            <>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Food</th>
                      <th>Qty</th>
                      <th>Calories</th>
                      <th>Protein</th>
                      <th>Carbs</th>
                      <th>Fat</th>
                    </tr>
                  </thead>
                  <tbody>
                    {previewRows.map((row) => (
                      <tr key={row.food}>
                        <td>{row.food}</td>
                        <td>{row.qty}</td>
                        <td>{row.calories}</td>
                        <td>{row.protein}</td>
                        <td>{row.carbs}</td>
                        <td>{row.fat}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="muted">
                Estimated totals: {previewRows.reduce((sum, row) => sum + row.calories, 0)} kcal | Protein{" "}
                {previewRows.reduce((sum, row) => sum + row.protein, 0)} g | Carbs{" "}
                {previewRows.reduce((sum, row) => sum + row.carbs, 0)} g | Fat{" "}
                {previewRows.reduce((sum, row) => sum + row.fat, 0)} g
              </p>
            </>
          ) : (
            <div className="empty">Select foods to preview meal totals.</div>
          )}
        </Card>

        <Card title="Suggested Foods For Your Goal">
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Food</th>
                  <th>Calories</th>
                  <th>Protein</th>
                  <th>Carbs</th>
                  <th>Fat</th>
                </tr>
              </thead>
              <tbody>
                {recommendations.map((item) => (
                  <tr key={item.food}>
                    <td>{item.food}</td>
                    <td>{item.calories}</td>
                    <td>{item.protein}</td>
                    <td>{item.carbs}</td>
                    <td>{item.fat}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      {analysis ? (
        <Card title="Nutrition Result">
          <StatGrid
            items={[
              { label: "Calories", value: `${analysis.calories} kcal` },
              { label: "Protein", value: `${analysis.protein} g` },
              { label: "Carbs", value: `${analysis.carbs} g` },
              { label: "Fat", value: `${analysis.fat} g` }
            ]}
          />

          <div style={{ marginTop: "1rem" }}>
            <div className="muted" style={{ marginBottom: "0.45rem" }}>
              Health Score: {analysis.health_score}/100
            </div>
            <ProgressBar value={analysis.health_score} />
          </div>

          <div className="chart-bars" style={{ marginTop: "1rem" }}>
            {[
              { label: "Protein", value: analysis.protein },
              { label: "Carbs", value: analysis.carbs },
              { label: "Fat", value: analysis.fat }
            ].map((item) => {
              const total = analysis.protein + analysis.carbs + analysis.fat || 1;
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

          <div className="list" style={{ marginTop: "1rem" }}>
            {getAnalysisSuggestions(analysis).map((suggestion) => (
              <div className="list-item" key={suggestion}>
                {suggestion}
              </div>
            ))}
          </div>

          <div style={{ marginTop: "1rem", display: "flex", gap: "0.8rem", flexWrap: "wrap" }}>
            <button
              className="button"
              onClick={() => {
                setDailyTotal({
                  calories: dailyTotal.calories + analysis.calories,
                  protein: dailyTotal.protein + analysis.protein,
                  carbs: dailyTotal.carbs + analysis.carbs,
                  fat: dailyTotal.fat + analysis.fat
                });
                addMealLogEntry({
                  meal: analysis.meal_type,
                  foods: analysis.foods.join(", "),
                  calories: analysis.calories,
                  protein: analysis.protein,
                  carbs: analysis.carbs,
                  fat: analysis.fat,
                  goal: analysis.goal
                });
              }}
            >
              Add to Daily Total
            </button>
          </div>
        </Card>
      ) : null}
    </div>
  );
}
