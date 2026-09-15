# Project Roadmap v2 — Data Analytics Track
## Comparative Sales Analytics & Forecasting System (Amazon vs Flipkart)

**Pivot note:** Project switched from a full-stack (Spring Boot + React) build to a pure data-analytics project on [this date]. The Spring Boot backend scaffold (`backend/`) is kept in the repo for history but is no longer being developed. Database layer stays on **PostgreSQL** (already populated and verified with real data) instead of MySQL — functionally equivalent for this stack.

## Tech Stack
| Tool | Use |
|---|---|
| Python | Main data analysis & preprocessing |
| Pandas | Data cleaning, transformation, merging |
| NumPy | Numerical calculations |
| Matplotlib | Sales/trend graphs |
| Seaborn | Statistical visualizations |
| Scikit-learn | ML models & evaluation |
| Prophet | Sales forecasting |
| PostgreSQL *(was MySQL)* | Store and query data |
| SQL | Sales/customer/product analysis |
| Power BI | Interactive dashboard |
| Jupyter Notebook | Python development & analysis |
| Git & GitHub | Version control |

## What carries over from the old roadmap (already done, still valid)
- Requirements doc, data dictionary, data quality report (`docs/`)
- Cleaned, standardized, merged datasets (`database/clean-data/`)
- PostgreSQL schema + 21,273 products / 20,333 reviews / 21,273 sales loaded and verified (`scripts/schema.sql`, `scripts/load_data.py`)
- SQL views for reporting (`scripts/views.sql`)

## New Phase Plan

### Phase A: Environment & EDA (Exploratory Data Analysis)
1. Set up Jupyter Notebook environment
2. Connect Python to PostgreSQL (via `psycopg2`/`sqlalchemy`)
3. Load data into Pandas DataFrames from the database (not raw CSVs — use the cleaned DB as source of truth)
4. Exploratory analysis: distributions, summary stats, missing data recheck
5. Visualize with Matplotlib/Seaborn: price distributions, rating distributions, category breakdowns

### Phase B: SQL-Driven Analysis
6. Write analytical SQL queries: revenue trends, category performance, platform comparison (builds on Day 26-29 queries already written)
7. Sales/customer/product deep-dive queries

### Phase C: Machine Learning
8. Sentiment analysis on Amazon reviews (scikit-learn or simple lexicon-based)
9. Sales forecasting with Prophet (using the synthetic `order_date` timeline)
10. Model evaluation (accuracy, RMSE, etc. as appropriate)

### Phase D: Power BI Dashboard
11. Connect Power BI to PostgreSQL
12. Build interactive dashboard: platform comparison, category trends, forecast visualization

### Phase E: Documentation & Submission
13. Consolidate Jupyter notebooks with clear narrative
14. Final report incorporating all findings
15. GitHub repo cleanup, README update, submission
