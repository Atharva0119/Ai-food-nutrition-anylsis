# Ai-food-nutrition-anylsis

AI-based Food Nutrition Analysis system that evaluates meals and provides health insights based on user goals like weight loss, maintenance, or muscle gain.

## Vercel-Ready Web App

This repo now includes a Next.js version of the app at the repo root for Vercel deployment.

### Run locally

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run dev
```

3. Open `http://localhost:3000`

### Notes

- The original Streamlit version is still kept in `ai-nutrition/` so you can compare behavior while migrating.
- The Vercel-ready app preserves the same core features:
  - Profile with BMI/TDEE-based calorie targets
  - Meal analysis and scoring
  - Daily dashboard and meal log export
  - Custom foods management
