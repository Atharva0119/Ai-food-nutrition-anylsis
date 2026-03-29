export type Goal = "Weight Loss" | "Muscle Gain" | "Maintain";
export type MealType = "Breakfast" | "Lunch" | "Dinner" | "Snack";
export type Gender = "Male" | "Female";
export type ActivityLevel =
  | "Sedentary"
  | "Lightly Active"
  | "Moderately Active"
  | "Very Active"
  | "Extra Active";

export type FoodItem = {
  food: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
};

export type DailyTotal = {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
};

export type MealLogEntry = {
  meal: MealType;
  foods: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  goal: Goal;
};

export type MealAnalysis = {
  foods: string[];
  quantities: Record<string, number>;
  goal: Goal;
  meal_type: MealType;
  target_calories: number;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  health_score: number;
};

export type UserProfile = {
  age: number;
  weight: number;
  height: number;
  gender: Gender;
  activity_level: ActivityLevel;
  goal: Goal;
};

export type ProfileSummary = {
  bmi: number;
  bmiCategory: string;
  bmr: number;
  tdee: number;
  targetCalories: number;
};
