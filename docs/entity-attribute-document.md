# Entity Attribute Document (Day 17)
## Comparative Sales Analytics & Forecasting System

---

## 1. Platform

| Attribute | Type | Constraints | Notes |
|---|---|---|---|
| platform_id | INT | PK, AUTO_INCREMENT | |
| name | VARCHAR(50) | NOT NULL, UNIQUE | "Amazon" / "Flipkart" |

**Row count:** 2 (seed data, not derived from CSV)

---

## 2. Category

| Attribute | Type | Constraints | Notes |
|---|---|---|---|
| category_id | INT | PK, AUTO_INCREMENT | |
| name | VARCHAR(100) | NOT NULL, UNIQUE | The 8 standardized categories from Day 13 (Electronics, Fashion, Home & Kitchen, Beauty & Personal Care, Automotive, Toys & Baby, Office & Stationery, Sports & Fitness, Other) |

**Row count:** 9 (seed data, derived from `standard_category` distinct values)

---

## 3. Product

| Attribute | Type | Constraints | Notes | Source column |
|---|---|---|---|---|
| product_pk | INT | PK, AUTO_INCREMENT | Internal surrogate key | new |
| id | VARCHAR(8) | UNIQUE | Original generated ID from Day 14 merge | products_final.id |
| platform_id | INT | FK -> Platform, NOT NULL | | products_final.platform (mapped) |
| category_id | INT | FK -> Category, NOT NULL | | products_final.category (mapped) |
| product_name | VARCHAR(500) | NOT NULL | | products_final.product_name |
| price | DECIMAL(10,2) | NOT NULL | Current selling price | products_final.price |
| mrp | DECIMAL(10,2) | NULLABLE | List price | products_final.mrp |
| discount_pct | DECIMAL(5,2) | NULLABLE | | products_final.discount_pct |
| rating | DECIMAL(2,1) | NULLABLE | NULL = genuinely unrated (esp. Flipkart) | products_final.rating |
| rating_count | INT | NULLABLE, DEFAULT 0 | NULL only for Flipkart (field doesn't exist there) | products_final.rating_count |
| brand | VARCHAR(255) | NULLABLE | NULL for all Amazon rows (no brand field); "Unknown" or NULL for ~29% of Flipkart | products_final.brand |
| image_url | VARCHAR(500) | NULLABLE | | products_final.image_url |
| source_url | VARCHAR(500) | NULLABLE | | products_final.source_url |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Record insert time (app-level, not from data) | new |

**Row count:** 21,273

---

## 4. Sales

*(Synthetic — derived from `order_date`, since neither platform provides real transaction history. This will be explicitly documented as simulated in the final report.)*

| Attribute | Type | Constraints | Notes | Source |
|---|---|---|---|---|
| sale_id | INT | PK, AUTO_INCREMENT | | new |
| product_pk | INT | FK -> Product, NOT NULL | | |
| order_date | DATE | NOT NULL | | products_final.order_date (Day 13) |
| quantity | INT | NOT NULL | To be generated Day 18: random 1-10, weighted toward 1-3 (realistic long-tail) | new (Day 18) |
| revenue | DECIMAL(12,2) | NOT NULL | Computed: price × quantity | derived |

**Row count:** 1 sale record per product initially (21,273) — can be expanded to multiple sales/product later if deeper time-series detail is needed for forecasting (Day 134+)

---

## 5. Review

| Attribute | Type | Constraints | Notes | Source column |
|---|---|---|---|---|
| review_pk | INT | PK, AUTO_INCREMENT | | new |
| product_pk | INT | FK -> Product, NOT NULL | Links via product_id match | reviews_final.product_id |
| reviewer_id | VARCHAR(100) | NULLABLE | | reviews_final.reviewer_id |
| reviewer_name | VARCHAR(255) | NULLABLE | | reviews_final.reviewer_name |
| review_title | VARCHAR(255) | NULLABLE | | reviews_final.review_title |
| review_content | TEXT | NULLABLE | Feeds sentiment analysis, Day 111+ | reviews_final.review_content |
| sentiment | VARCHAR(20) | NULLABLE | Populated later (Day 111-112): Positive/Negative/Neutral | new (Phase 4) |
| is_fake | BOOLEAN | NULLABLE | Populated later (Day 161-165): fake review detection | new (Phase 6) |
| fake_confidence | DECIMAL(5,2) | NULLABLE | Confidence score for is_fake prediction | new (Phase 6) |

**Row count:** 20,333 (Amazon only)

---

## 6. User

*(Application authentication — not derived from Kaggle data.)*

| Attribute | Type | Constraints | Notes |
|---|---|---|---|
| user_id | INT | PK, AUTO_INCREMENT | |
| username | VARCHAR(100) | NOT NULL, UNIQUE | |
| password | VARCHAR(255) | NOT NULL | BCrypt hash, never plain text |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'VIEWER' | 'ADMIN' or 'VIEWER' |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | |

**Row count:** 0 initially (created via registration, Day 97+)

---

## Relationship Summary

```
Platform (1) ----< (many) Product
Category (1) ----< (many) Product
Product  (1) ----< (many) Sales
Product  (1) ----< (many) Review
User: standalone (no FK relationship to e-commerce data)
```

This is the attribute set that Day 18's ER diagram and Day 20's schema design will be built directly from.
