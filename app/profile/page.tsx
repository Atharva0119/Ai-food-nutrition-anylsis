"use client";

import { useState } from "react";

import { Card, Hero, StatGrid } from "@/components/ui";
import { useAppState } from "@/lib/app-state";
import { ACTIVITY_LEVELS, GOALS, getProfileSummary } from "@/lib/nutrition";

export default function ProfilePage() {
  const { setUserProfile, userProfile } = useAppState();
  const [form, setForm] = useState(userProfile);
  const summary = getProfileSummary(form);

  return (
    <div className="page-stack">
      <Hero
        title="Profile"
        subtitle="Set your body stats, activity level, and goal so the rest of the app can personalize calorie targets automatically."
        pills={["BMI", "BMR", "TDEE", "Smart targets"]}
      />

      <div className="two-grid">
        <Card title="Body Profile">
          <div className="form-grid">
            <div className="field">
              <label>Age</label>
              <input type="number" value={form.age} onChange={(e) => setForm({ ...form, age: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Weight (kg)</label>
              <input type="number" value={form.weight} step="0.5" onChange={(e) => setForm({ ...form, weight: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Height (cm)</label>
              <input type="number" value={form.height} step="0.5" onChange={(e) => setForm({ ...form, height: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Gender</label>
              <select value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value as typeof form.gender })}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
            <div className="field">
              <label>Activity Level</label>
              <select
                value={form.activity_level}
                onChange={(e) => setForm({ ...form, activity_level: e.target.value as typeof form.activity_level })}
              >
                {ACTIVITY_LEVELS.map((activity) => (
                  <option key={activity} value={activity}>
                    {activity}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Goal</label>
              <select value={form.goal} onChange={(e) => setForm({ ...form, goal: e.target.value as typeof form.goal })}>
                {GOALS.map((goal) => (
                  <option key={goal} value={goal}>
                    {goal}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ marginTop: "1rem" }}>
            <button className="button" onClick={() => setUserProfile(form)}>
              Save Profile
            </button>
          </div>
        </Card>

        <Card title="Profile Output">
          <StatGrid
            items={[
              { label: "BMI", value: summary.bmi.toFixed(1) },
              { label: "BMI Category", value: summary.bmiCategory },
              { label: "BMR", value: `${summary.bmr} kcal` },
              { label: "TDEE", value: `${summary.tdee} kcal` }
            ]}
          />
          <div className="list" style={{ marginTop: "1rem" }}>
            <div className="list-item">Suggested calorie target: {summary.targetCalories} kcal</div>
            <div className="list-item">Goal: {form.goal}</div>
            <div className="list-item">Activity level: {form.activity_level}</div>
          </div>
        </Card>
      </div>
    </div>
  );
}
