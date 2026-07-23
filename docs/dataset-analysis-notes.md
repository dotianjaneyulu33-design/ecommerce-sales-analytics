# Dataset Analysis Notes (Day 9)

## Amazon Dataset — `amazon.csv`
**Shape:** 1,465 rows × 16 columns

| Column | Type | Notes / Issues |
|---|---|---|
| product_id | text | 114 duplicate IDs (1,351 unique / 1,465 rows) |
| product_name | text | Clean |
| category | text | Pipe-separated hierarchy. Top segments: Electronics (526), Computers&Accessories (453), Home&Kitchen (448), Office Products (31), + 5 minor categories |
| discounted_price | text (numeric) | Stored as `₹399` — has currency symbol, needs cleaning |
| actual_price | text (numeric) | Stored as `₹1,099` — has currency symbol + commas, needs cleaning |
| discount_percentage | text (numeric) | Stored as `64%` — needs `%` stripped |
| rating | text (numeric) | 1 corrupted value (`"|"` for product B08L12N5H1) |
| rating_count | text (numeric) | Has commas (`24,269`); 2 missing values |
| about_product | text | Clean |
| user_id / user_name / review_id / review_title / review_content | text | Comma-separated lists — multiple reviews bundled per product row. Needs exploding into separate review rows |
| img_link / product_link | text | Clean |

**No transaction date or order-quantity field** — snapshot data only.

---

## Flipkart Dataset — `flipkart_com-ecommerce_sample.csv`
**Shape:** 20,000 rows × 15 columns

| Column | Type | Notes / Issues |
|---|---|---|
| uniq_id | text | Fully unique, good primary key |
| crawl_timestamp | text | All from 2016; not a real sales date |
| product_name | text | Clean |
| product_category_tree | text | Messy JSON-array-style string, `>>` separated. Top categories: Clothing (6,198), Jewellery (3,531), Footwear (1,227), Mobiles & Accessories (1,099), Automotive (1,012) |
| retail_price | numeric | 78 missing values |
| discounted_price | numeric | 78 missing values (same rows) |
| brand | text | 5,864 missing (29%) |
| product_rating / overall_rating | text (numeric) | **91% (18,151/20,000) say "No rating available"** — major gap |
| product_specifications | text | Messy pseudo-JSON (Ruby hash syntax), 14 missing |
| description | text | 2 missing |

**No review text, no transaction date/quantity field** — snapshot data only.

---

## Key Cross-Dataset Findings

1. **Category mismatch:** Amazon sample is electronics/computers-heavy; Flipkart sample is fashion/jewellery-heavy. Fair category-level comparison is only strong where both overlap (Electronics, Home & Kitchen, Beauty/Personal Care). This limitation should be stated explicitly in the final report.
2. **No real sales transactions in either dataset** — both are product-listing snapshots. The `Sales` entity (Day 38) will require **simulated/synthetic order data** (realistic random dates/quantities per product) to support time-series analysis and forecasting (Day 134+). This must be clearly labeled as synthetic in documentation, not presented as real sales history.
3. **Amazon has duplicate product rows** — de-duplicate by `product_id` before loading into the DB.
4. **Flipkart ratings are 91% missing** — treat as "unrated" category rather than dropping most of the dataset.
5. **Price formats differ:** Amazon prices are text with currency symbols/commas; Flipkart prices are already numeric. Different cleaning logic needed per source.
6. **Amazon reviews are bundled** (comma-separated lists in one cell); Flipkart has no review text at all — sentiment analysis (Day 111+) will rely primarily on the Amazon review data.
