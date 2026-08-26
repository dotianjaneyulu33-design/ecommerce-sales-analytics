# Comparative Sales Analytics & Forecasting System

Full-stack analytics platform comparing Amazon vs Flipkart sales, pricing, and customer sentiment.

**Status:** Phase 1 (Data & Database) complete — Day 30 of 210-day roadmap

## Tech Stack
- **Backend:** Java, Spring Boot, Spring Data JPA, Spring Security (planned)
- **Database:** PostgreSQL *(switched from MySQL on Day 21 due to local environment issues — see `docs/database-schema-postgres.md`)*
- **Frontend:** React, Chart.js/Recharts (planned)
- **ML:** Python (Flask/FastAPI, scikit-learn, Prophet) (planned)

## Project Structure
```
backend/        - Spring Boot application (Phase 2, Day 31+)
frontend/        - React dashboard (Phase 3, Day 61+)
ml-service/       - Python ML microservice (Phase 4+, Day 104+)
database/          - Raw data, cleaned data (git-ignored), and data pipeline
  raw-data/           - Original Kaggle datasets (git-ignored)
  clean-data/          - Cleaned/standardized/merged CSVs (git-ignored, regenerate via scripts/)
scripts/             - Python data cleaning scripts + SQL schema/views
docs/                - Requirements, data dictionary, ER diagram, reports
```

## Data Sources
- Amazon Sales Dataset (Kaggle, karkavelrajaj) — 1,465 raw products
- Flipkart E-commerce Dataset (Kaggle, PromptCloudHQ) — 20,000 raw products

See `docs/data-sources.md` and `docs/dataset-analysis-notes.md` for details.

## Database
- **21,273 products**, **20,333 reviews**, **21,273 synthetic sales records** loaded and verified
- Full schema: `docs/database-schema-postgres.md`
- ER diagram: `docs/er-diagram.drawio`
- Setup scripts: `scripts/schema.sql`, `scripts/views.sql`, `scripts/load_data.py`

## Key Findings So Far
- Amazon products in this sample: fewer (1,351), pricier on average, higher rated
- Flipkart products: far more numerous (19,922), especially Fashion-heavy
- Electronics and Home & Kitchen are the only categories with strong representation on both platforms — most reliable for fair comparison
- See `docs/database-verification-report.md` for full findings

## Roadmap
Following a 210-day full-stack build plan: Data & DB (Days 1-30) → Backend APIs (31-60) → Frontend Dashboard (61-90) → Security & Sentiment ML (91-120) → Price Analytics & Forecasting (121-150) → Fake Review Detection & Advanced Features (151-180) → Deployment & Submission (181-210).
