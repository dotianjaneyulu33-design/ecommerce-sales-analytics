# Data Dictionary (Day 10)
## Comparative Sales Analytics & Forecasting System

This dictionary documents every column in both raw source datasets, its meaning, its data type (raw and target), and which future database entity/table it will feed into (per the entities identified on Day 16: Platform, Category, Product, Sales, Review).

---

## Source: `amazon.csv` (Amazon Sales Dataset)

| Column | Meaning | Raw Type | Target Type | Maps To (future entity) | Cleaning Needed |
|---|---|---|---|---|---|
| product_id | Amazon's unique product identifier (ASIN) | text | VARCHAR (PK candidate) | Product.platform_product_id | De-duplicate (114 dupes found) |
| product_name | Product title | text | VARCHAR(500) | Product.name | Trim whitespace |
| category | Pipe-separated category hierarchy | text | — (parsed) | Category.name (top segment) | Split on `\|`, take first segment as top-level category |
| discounted_price | Current selling price | text (`₹399`) | DECIMAL(10,2) | Product.price | Strip `₹`, strip commas, cast to float |
| actual_price | List price / MRP | text (`₹1,099`) | DECIMAL(10,2) | Product.mrp | Strip `₹`, strip commas, cast to float |
| discount_percentage | Discount off MRP | text (`64%`) | DECIMAL(5,2) | Product.discount_pct | Strip `%`, cast to float |
| rating | Average customer rating | text | DECIMAL(2,1) | Product.avg_rating | Fix 1 corrupted value (`"\|"`); cast to float |
| rating_count | Number of ratings | text (`24,269`) | INT | Product.rating_count | Strip commas, cast to int; impute 2 missing |
| about_product | Bullet-point description | text | TEXT | Product.description | None |
| user_id | Comma-separated list of reviewer IDs | text (list) | VARCHAR (per row after explode) | Review.reviewer_id | Split on comma, explode to one row per review |
| user_name | Comma-separated list of reviewer names | text (list) | VARCHAR (per row after explode) | Review.reviewer_name | Split on comma, explode |
| review_id | Comma-separated list of review IDs | text (list) | VARCHAR (per row after explode) | Review.review_id | Split on comma, explode |
| review_title | Comma-separated list of review titles | text (list) | VARCHAR(255) (per row after explode) | Review.title | Split on comma, explode |
| review_content | Comma-separated list of review bodies | text (list) | TEXT (per row after explode) | Review.content | Split on comma, explode (note: contains embedded commas — must split carefully, ideally by matching position across the parallel list columns rather than naive comma-split) |
| img_link | Product image URL | text | VARCHAR(500) | Product.image_url | None |
| product_link | Product page URL | text | VARCHAR(500) | Product.source_url | None |

**Platform value for all rows:** `Amazon` (constant, not in source file — added during load)

---

## Source: `flipkart_com-ecommerce_sample.csv` (Flipkart E-commerce Dataset)

| Column | Meaning | Raw Type | Target Type | Maps To (future entity) | Cleaning Needed |
|---|---|---|---|---|---|
| uniq_id | Unique row/product identifier | text | VARCHAR (PK candidate) | Product.platform_product_id | None (already unique) |
| crawl_timestamp | Date/time the listing was scraped | text | DATETIME | *(metadata only — not a sales date)* | None, but do not use as Sales.date |
| product_url | Product page link | text | VARCHAR(500) | Product.source_url | None |
| product_name | Product title | text | VARCHAR(500) | Product.name | Trim whitespace |
| product_category_tree | Full category path | text (JSON-array-style) | — (parsed) | Category.name (top segment) | Strip `["`/`"]`, split on `>>`, take first segment |
| pid | Flipkart's internal product ID | text | VARCHAR | (secondary ID, optional) | None |
| retail_price | MRP | numeric | DECIMAL(10,2) | Product.mrp | 78 missing — impute or exclude |
| discounted_price | Selling price | numeric | DECIMAL(10,2) | Product.price | 78 missing — impute or exclude |
| image | List of image URLs (JSON-array-style) | text | VARCHAR(500) | Product.image_url | Parse array, take first URL |
| is_FK_Advantage_product | Flipkart Advantage program flag | boolean text | BOOLEAN | Product.is_featured (optional) | Cast to boolean |
| description | Long-form product description | text | TEXT | Product.description | 2 missing |
| product_rating | Product-level rating | text (`"No rating available"` or number) | DECIMAL(2,1), nullable | Product.avg_rating | 91% say "No rating available" → convert to NULL, keep as unrated |
| overall_rating | Seller/overall rating (mirrors product_rating in this dataset) | text | DECIMAL(2,1), nullable | Product.avg_rating (fallback) | Same as above |
| brand | Brand name | text | VARCHAR(255) | Product.brand | 29% missing — allow NULL |
| product_specifications | Pseudo-JSON key-value spec list | text (Ruby-hash-style string) | — (optional parsed JSON) | Product.specifications (optional JSON column) | Custom parser needed if used; otherwise can be excluded from MVP scope |

**Platform value for all rows:** `Flipkart` (constant, not in source file — added during load)

---

## Cross-Dataset Notes

- **Category taxonomy mismatch:** Amazon top categories (Electronics, Computers&Accessories, Home&Kitchen) and Flipkart top categories (Clothing, Jewellery, Footwear, Mobiles & Accessories) barely overlap. A `Category` mapping table will be needed to normalize both onto a shared taxonomy (e.g., mapping "Computers&Accessories" and "Mobiles & Accessories" both to "Electronics").
- **No native Sales/transaction data** in either source — the `Sales` table will be populated with **synthetic order records** (random dates/quantities generated per product, documented as simulated data).
- **Platform** is not a column in either file — it will be injected as a constant value (`'Amazon'` / `'Flipkart'`) during the data-loading step, matching the `Platform` entity identified on Day 16.
