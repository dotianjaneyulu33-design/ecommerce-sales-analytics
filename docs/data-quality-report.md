# Data Quality Report (Day 11)
## Comparative Sales Analytics & Forecasting System

Generated from raw source files: `amazon.csv` (1,465 rows) and `flipkart_com-ecommerce_sample.csv` (20,000 rows).

---

## 1. Duplicate Records

| Dataset | Duplicate type | Count | Remediation |
|---|---|---|---|
| Amazon | Duplicate `product_id` (same product listed twice) | 114 rows | Drop duplicates, keep first occurrence: `df.drop_duplicates(subset='product_id', keep='first')` |
| Amazon | Fully duplicate rows (all columns identical) | 0 | None needed |
| Flipkart | Duplicate `uniq_id` | 0 | None needed |
| Flipkart | Fully duplicate rows | 0 | None needed |

**Impact:** Amazon dataset effectively has 1,351 unique products, not 1,465. Row count will drop by ~7.8% after de-duplication — expected and correct.

---

## 2. Missing Values

### Amazon (`amazon.csv`, 1,465 rows)

| Column | Missing count | % | Remediation |
|---|---|---|---|
| rating_count | 2 | 0.14% | Impute with 0 (no ratings yet) or median of category — recommend 0, since a missing count on a rated product is more likely "not yet counted" than data-entry error |
| rating | 1 corrupted (`"\|"` value, not a standard NaN) | 0.07% | Set to NULL, then impute with category average rating |

All other Amazon columns: 0 missing.

### Flipkart (`flipkart_com-ecommerce_sample.csv`, 20,000 rows)

| Column | Missing count | % | Remediation |
|---|---|---|---|
| retail_price | 78 | 0.39% | Exclude these 78 rows from price-based analysis (both price fields missing together — likely delisted/incomplete listings, not worth imputing) |
| discounted_price | 78 | 0.39% | Same 78 rows as above — confirmed overlapping |
| brand | 5,864 | 29.3% | Keep as NULL / "Unknown" — too large a gap to impute reliably; exclude from brand-level analysis only |
| description | 2 | 0.01% | Leave as NULL, not used in core comparison metrics |
| product_specifications | 14 | 0.07% | Leave as NULL — this field is optional/stretch scope anyway |
| image | 3 | 0.02% | Leave as NULL, use a placeholder image in the frontend if needed |
| product_rating / overall_rating | 18,151 marked `"No rating available"` (not a true NULL, but functionally missing) | 90.8% | **Major gap.** Convert `"No rating available"` → NULL. Do not impute — treat "unrated" as a valid, meaningful state (e.g., show as "Not yet rated" in the UI) rather than manufacturing a fake average. Any rating-based comparison chart should note it's based on the ~1,850 rated products only. |

---

## 3. Format / Type Issues (not missing, but invalid for direct use)

| Dataset | Column | Issue |
|---|---|---|
| Amazon | discounted_price, actual_price | Stored as text with ₹ symbol and commas (e.g. `₹1,099`) — must be cleaned to numeric before any calculation |
| Amazon | discount_percentage | Stored as text with `%` (e.g. `64%`) |
| Amazon | rating_count | Has thousands-separator commas (e.g. `24,269`) |
| Flipkart | product_category_tree | JSON-array-style string requiring parsing, not a clean category field |
| Flipkart | product_specifications | Pseudo-JSON with Ruby hash syntax (`=>`), requires custom parsing |

---

## 4. Structural Issue (beyond standard missing/duplicate checks)

**Amazon review columns** (`user_id`, `user_name`, `review_id`, `review_title`, `review_content`) each contain a **comma-separated list of multiple reviews bundled into a single cell per product**, rather than one row per review. This isn't a missing-value or duplicate issue in the traditional sense, but it must be resolved (exploded into individual review rows) before this data can populate a normalized `Review` table. Flagged here for visibility into Day 12 cleaning work.

---

## 5. Summary — Priority Order for Day 12 Cleaning

1. **Amazon:** drop 114 duplicate `product_id` rows
2. **Amazon:** clean price/percentage/count fields (strip ₹, %, commas → cast to numeric)
3. **Amazon:** fix 1 corrupted rating value, impute 2 missing rating_counts
4. **Amazon:** explode bundled review columns into individual review rows
5. **Flipkart:** exclude/flag 78 rows with missing prices
6. **Flipkart:** convert `"No rating available"` → NULL in both rating columns
7. **Flipkart:** leave `brand`, `description`, `product_specifications`, `image` NULLs as-is (not critical path)
8. Both: parse category hierarchy strings into clean top-level category values
