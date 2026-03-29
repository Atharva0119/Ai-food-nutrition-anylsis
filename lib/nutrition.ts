import baseFoodData from "@/lib/food-data.json";
import type {
  ActivityLevel,
  DailyTotal,
  FoodItem,
  Goal,
  MealAnalysis,
  MealType,
  ProfileSummary,
  UserProfile
} from "@/lib/types";

export const DEFAULT_DAILY_TOTAL: DailyTotal = {
  calories: 0,
  protein: 0,
  carbs: 0,
  fat: 0
};

export const DEFAULT_PROFILE: UserProfile = {
  age: 25,
  weight: 70,
  height: 170,
  gender: "Male",
  activity_level: "Moderately Active",
  goal: "Maintain"
};

export const GOALS: Goal[] = ["Weight Loss", "Muscle Gain", "Maintain"];
export const MEAL_TYPES: MealType[] = ["Breakfast", "Lunch", "Dinner", "Snack"];
export const ACTIVITY_LEVELS: ActivityLevel[] = [
  "Sedentary",
  "Lightly Active",
  "Moderately Active",
  "Very Active",
  "Extra Active"
];

export const ACTIVITY_MULTIPLIERS: Record<ActivityLevel, number> = {
  Sedentary: 1.2,
  "Lightly Active": 1.375,
  "Moderately Active": 1.55,
  "Very Active": 1.725,
  "Extra Active": 1.9
};

export const BASE_FOODS = baseFoodData as FoodItem[];

export function getFoodData(customFoods: FoodItem[]): FoodItem[] {
  return [...BASE_FOODS, ...customFoods];
}

export function calculateBMI(weightKg: number, heightCm: number) {
  const heightM = heightCm / 100;
  if (!heightM) return 0;
  return weightKg / (heightM * heightM);
}

export function getBmiCategory(bmi: number) {
  if (bmi < 18.5) return "Underweight";
  if (bmi < 25) return "Normal";
  if (bmi < 30) return "Overweight";
  return "Obese";
}

export function calculateBMR(profile: UserProfile) {
  const { age, height, weight, gender } = profile;
  if (gender === "Male") {
    return 10 * weight + 6.25 * height - 5 * age + 5;
  }
  return 10 * weight + 6.25 * height - 5 * age - 161;
}

export function calculateTDEE(profile: UserProfile) {
  return calculateBMR(profile) * ACTIVITY_MULTIPLIERS[profile.activity_level];
}

export function getPersonalizedTarget(profile: UserProfile) {
  const tdee = calculateTDEE(profile);
  if (profile.goal === "Weight Loss") return Math.max(1200, Math.round(tdee - 400));
  if (profile.goal === "Muscle Gain") return Math.round(tdee + 300);
  return Math.round(tdee);
}

export function getProfileSummary(profile: UserProfile): ProfileSummary {
  const bmi = calculateBMI(profile.weight, profile.height);
  return {
    bmi,
    bmiCategory: getBmiCategory(bmi),
    bmr: Math.round(calculateBMR(profile)),
    tdee: Math.round(calculateTDEE(profile)),
    targetCalories: getPersonalizedTarget(profile)
  };
}

export function getGoalRecommendations(foodData: FoodItem[], goal: Goal) {
  const enhanced = [...foodData].map((item) => ({
    ...item,
    proteinDensity: item.protein / Math.max(item.calories, 1)
  }));

  if (goal === "Weight Loss") {
    enhanced.sort((a, b) => a.calories - b.calories || b.proteinDensity - a.proteinDensity);
  } else if (goal === "Muscle Gain") {
    enhanced.sort((a, b) => b.protein - a.protein || b.calories - a.calories);
  } else {
    enhanced.sort((a, b) => b.proteinDensity - a.proteinDensity || a.calories - b.calories);
  }

  return enhanced.slice(0, 5);
}

export function analyzeMeal(
  foodData: FoodItem[],
  foods: string[],
  quantities: Record<string, number>,
  goal: Goal,
  mealType: MealType,
  targetCalories: number
): MealAnalysis {
  let calories = 0;
  let protein = 0;
  let carbs = 0;
  let fat = 0;

  foods.forEach((foodName) => {
    const food = foodData.find((item) => item.food === foodName);
    if (!food) return;
    const qty = quantities[foodName] ?? 1;
    calories += food.calories * qty;
    protein += food.protein * qty;
    carbs += food.carbs * qty;
    fat += food.fat * qty;
  });

  let healthScore = 0;
  if (goal === "Weight Loss") {
    if (calories <= 300) healthScore += 50;
    if (protein >= 5) healthScore += 30;
    if (carbs < 50) healthScore += 20;
  } else if (goal === "Muscle Gain") {
    if (protein >= 15) healthScore += 50;
    if (calories >= 300) healthScore += 30;
    if (fat < 20) healthScore += 20;
  } else {
    if (calories < 500) healthScore += 50;
    if (protein >= 5) healthScore += 25;
    if (carbs < 60) healthScore += 25;
  }

  return {
    foods,
    quantities,
    goal,
    meal_type: mealType,
    target_calories: targetCalories,
    calories,
    protein,
    carbs,
    fat,
    health_score: healthScore
  };
}

export function getDailyWarnings(tracker: DailyTotal, targetCalories: number) {
  const warnings: string[] = [];
  if (tracker.calories > targetCalories) {
    warnings.push("You have exceeded your daily calorie target.");
  } else if (tracker.calories > 0.8 * targetCalories) {
    warnings.push("You are close to your daily calorie limit.");
  }

  if (tracker.protein < 40) warnings.push("Protein intake is low today. Consider adding protein-rich foods.");
  if (tracker.carbs > 200) warnings.push("Carbohydrate intake is relatively high today.");
  if (!warnings.length) warnings.push("Great job! Your daily intake is balanced so far.");
  return warnings;
}

export function getAnalysisSuggestions(analysis: MealAnalysis) {
  const suggestions: string[] = [];
  if (analysis.protein < 15) suggestions.push("Increase protein intake: add eggs, paneer, chicken breast, or curd.");
  if (analysis.carbs > 60) suggestions.push("Carbs are high: next meal should be lighter, such as salad, fruits, or protein-rich food.");
  if (analysis.calories > 400) suggestions.push("High calorie intake: keep next meal low calorie.");
  if (analysis.goal === "Muscle Gain" && analysis.protein < 20) suggestions.push("For muscle gain, focus on high-protein foods in the next meal.");
  if (analysis.goal === "Weight Loss" && analysis.calories > 300) suggestions.push("For weight loss, next meal should be low-calorie and high in fiber.");
  if (!suggestions.length) suggestions.push("Great balance! Maintain similar food choices for the next meal.");
  return suggestions;
}
