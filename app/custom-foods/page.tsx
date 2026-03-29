"use client";

import { useMemo, useState } from "react";

import { Card, Hero, StatGrid } from "@/components/ui";
import { useAppState } from "@/lib/app-state";
import { BASE_FOODS, getFoodData } from "@/lib/nutrition";
import type { FoodItem } from "@/lib/types";

const initialFood: FoodItem = {
  food: "",
  calories: 100,
  protein: 5,
  carbs: 10,
  fat: 3
};

export default function CustomFoodsPage() {
  const { addCustomFood, customFoods } = useAppState();
  const [form, setForm] = useState<FoodItem>(initialFood);
  const [search, setSearch] = useState("");
  const foodData = useMemo(() => getFoodData(customFoods), [customFoods]);

  const filteredFoods = foodData.filter((item) => item.food.toLowerCase().includes(search.toLowerCase()));

  const handleAdd = () => {
    const normalizedName = form.food.trim().toLowerCase();
    if (!normalizedName) return;
    const exists = foodData.some((item) => item.food.toLowerCase() === normalizedName);
    if (exists) return;
    addCustomFood({ ...form, food: form.food.trim() });
    setForm(initialFood);
  };

  return (
    <div className="page-stack">
      <Hero
        title="Custom Foods"
        subtitle="Expand the nutrition database with your own foods so meal analysis fits your real eating habits."
        pills={["Food studio", "Reusable entries", "Personalized database"]}
      />

      <StatGrid
        items={[
          { label: "Base Foods", value: BASE_FOODS.length },
          { label: "Custom Foods", value: customFoods.length },
          { label: "Total Foods", value: foodData.length }
        ]}
      />

      <div className="two-grid">
        <Card title="Add Custom Food">
          <div className="form-grid">
            <div className="field" style={{ gridColumn: "1 / -1" }}>
              <label>Food Name</label>
              <input value={form.food} onChange={(e) => setForm({ ...form, food: e.target.value })} placeholder="e.g. Greek yogurt bowl" />
            </div>
            <div className="field">
              <label>Calories</label>
              <input type="number" value={form.calories} onChange={(e) => setForm({ ...form, calories: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Protein (g)</label>
              <input type="number" value={form.protein} onChange={(e) => setForm({ ...form, protein: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Carbs (g)</label>
              <input type="number" value={form.carbs} onChange={(e) => setForm({ ...form, carbs: Number(e.target.value) })} />
            </div>
            <div className="field">
              <label>Fat (g)</label>
              <input type="number" value={form.fat} onChange={(e) => setForm({ ...form, fat: Number(e.target.value) })} />
            </div>
          </div>

          <div style={{ marginTop: "1rem" }}>
            <button className="button" onClick={handleAdd}>
              Add Food
            </button>
          </div>
        </Card>

        <Card title="Your Custom Foods">
          {customFoods.length ? (
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
                  {customFoods.map((food) => (
                    <tr key={food.food}>
                      <td>{food.food}</td>
                      <td>{food.calories}</td>
                      <td>{food.protein}</td>
                      <td>{food.carbs}</td>
                      <td>{food.fat}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="empty">You have not added any custom foods yet.</div>
          )}
        </Card>
      </div>

      <Card title="Full Food Database">
        <div className="field" style={{ marginBottom: "1rem" }}>
          <label>Search all foods</label>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Type a food name" />
        </div>

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
              {filteredFoods.map((food) => (
                <tr key={food.food}>
                  <td>{food.food}</td>
                  <td>{food.calories}</td>
                  <td>{food.protein}</td>
                  <td>{food.carbs}</td>
                  <td>{food.fat}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
