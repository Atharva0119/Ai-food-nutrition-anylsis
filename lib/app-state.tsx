"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";

import {
  DEFAULT_DAILY_TOTAL,
  DEFAULT_PROFILE
} from "@/lib/nutrition";
import type { DailyTotal, FoodItem, MealAnalysis, MealLogEntry, UserProfile } from "@/lib/types";

type AppStore = {
  customFoods: FoodItem[];
  mealLog: MealLogEntry[];
  dailyTotal: DailyTotal;
  lastAnalysis: MealAnalysis | null;
  userProfile: UserProfile;
  setCustomFoods: (foods: FoodItem[]) => void;
  addCustomFood: (food: FoodItem) => void;
  setMealLog: (entries: MealLogEntry[]) => void;
  addMealLogEntry: (entry: MealLogEntry) => void;
  setDailyTotal: (daily: DailyTotal) => void;
  resetDailyTotal: () => void;
  setLastAnalysis: (analysis: MealAnalysis | null) => void;
  setUserProfile: (profile: UserProfile) => void;
};

const STORAGE_KEY = "ai-nutrition-web-state";

const AppStateContext = createContext<AppStore | null>(null);

export function AppStateProvider({ children }: { children: React.ReactNode }) {
  const [customFoods, setCustomFoods] = useState<FoodItem[]>([]);
  const [mealLog, setMealLog] = useState<MealLogEntry[]>([]);
  const [dailyTotal, setDailyTotal] = useState<DailyTotal>(DEFAULT_DAILY_TOTAL);
  const [lastAnalysis, setLastAnalysis] = useState<MealAnalysis | null>(null);
  const [userProfile, setUserProfile] = useState<UserProfile>(DEFAULT_PROFILE);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    try {
      const raw = window.localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<AppStore>;
        setCustomFoods(parsed.customFoods ?? []);
        setMealLog(parsed.mealLog ?? []);
        setDailyTotal(parsed.dailyTotal ?? DEFAULT_DAILY_TOTAL);
        setLastAnalysis(parsed.lastAnalysis ?? null);
        setUserProfile(parsed.userProfile ?? DEFAULT_PROFILE);
      }
    } catch {
      // Ignore corrupted local state and continue with defaults.
    } finally {
      setHydrated(true);
    }
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ customFoods, mealLog, dailyTotal, lastAnalysis, userProfile })
    );
  }, [customFoods, dailyTotal, hydrated, lastAnalysis, mealLog, userProfile]);

  const value = useMemo<AppStore>(
    () => ({
      customFoods,
      mealLog,
      dailyTotal,
      lastAnalysis,
      userProfile,
      setCustomFoods,
      addCustomFood: (food) => setCustomFoods((current) => [...current, food]),
      setMealLog,
      addMealLogEntry: (entry) => setMealLog((current) => [...current, entry]),
      setDailyTotal,
      resetDailyTotal: () => {
        setDailyTotal(DEFAULT_DAILY_TOTAL);
        setMealLog([]);
        setLastAnalysis(null);
      },
      setLastAnalysis,
      setUserProfile
    }),
    [customFoods, dailyTotal, lastAnalysis, mealLog, userProfile]
  );

  return <AppStateContext.Provider value={value}>{children}</AppStateContext.Provider>;
}

export function useAppState() {
  const context = useContext(AppStateContext);
  if (!context) {
    throw new Error("useAppState must be used within AppStateProvider");
  }
  return context;
}
