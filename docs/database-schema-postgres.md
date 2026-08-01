# Database Schema Document (Day 20 — Revised for PostgreSQL)
## Comparative Sales Analytics & Forecasting System

**Note:** Project switched from MySQL to PostgreSQL after Day 21 setup issues. All syntax below is PostgreSQL-compatible.

Database name: `ecommerce_analytics`
Encoding: `UTF8` (PostgreSQL default — supports full Unicode)

---

## Full DDL

```sql
CREATE DATABASE ecommerce_analytics
  ENCODING 'UTF8';

-- Connect to it before running the rest:
-- \c ecommerce_analytics

-- ========================================
-- 1. PLATFORM
-- ========================================
CREATE TABLE platform (
    platform_id   SERIAL PRIMARY KEY,
    name          VARCHAR(50) NOT NULL UNIQUE
);

-- ========================================
-- 2. CATEGORY
-- ========================================
CREATE TABLE category (
    category_id   SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL UNIQUE
);

-- ========================================
-- 3. PRODUCT
-- ========================================
CREATE TABLE product (
    product_pk       SERIAL PRIMARY KEY,
    id               VARCHAR(8) UNIQUE,
    platform_id      INT NOT NULL REFERENCES platform(platform_id) ON DELETE RESTRICT,
    category_id      INT NOT NULL REFERENCES category(category_id) ON DELETE RESTRICT,
    product_name     VARCHAR(500) NOT NULL,
    price            DECIMAL(10,2) NOT NULL,
    mrp              DECIMAL(10,2),
    discount_pct     DECIMAL(5,2),
    rating           DECIMAL(2,1),
    rating_count     INT DEFAULT 0,
    brand            VARCHAR(255),
    image_url        VARCHAR(500),
    source_url       VARCHAR(500),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_product_platform ON product(platform_id);
CREATE INDEX idx_product_category ON product(category_id);
CREATE INDEX idx_product_rating ON product(rating);

-- ========================================
-- 4. SALES
-- ========================================
CREATE TABLE sales (
    sale_id       SERIAL PRIMARY KEY,
    product_pk    INT NOT NULL REFERENCES product(product_pk) ON DELETE CASCADE,
    order_date    DATE NOT NULL,
    quantity      INT NOT NULL,
    revenue       DECIMAL(12,2) NOT NULL
);

CREATE INDEX idx_sales_product ON sales(product_pk);
CREATE INDEX idx_sales_date ON sales(order_date);

-- ========================================
-- 5. REVIEW
-- ========================================
CREATE TABLE review (
    review_pk         SERIAL PRIMARY KEY,
    product_pk        INT NOT NULL REFERENCES product(product_pk) ON DELETE CASCADE,
    reviewer_id        VARCHAR(100),
    reviewer_name       VARCHAR(255),
    review_title        VARCHAR(255),
    review_content       TEXT,
    sentiment            VARCHAR(20),
    is_fake               BOOLEAN,
    fake_confidence        DECIMAL(5,2)
);

CREATE INDEX idx_review_product ON review(product_pk);
CREATE INDEX idx_review_sentiment ON review(sentiment);

-- ========================================
-- 6. USER (application authentication)
-- ========================================
CREATE TABLE app_user (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(100) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    role          VARCHAR(20) NOT NULL DEFAULT 'VIEWER' CHECK (role IN ('ADMIN', 'VIEWER')),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## What changed from the MySQL version

| MySQL | PostgreSQL | Why |
|---|---|---|
| `AUTO_INCREMENT` | `SERIAL` | Postgres's auto-increment mechanism |
| `ENGINE=InnoDB` | *(removed)* | Not a Postgres concept — Postgres always supports FKs/transactions natively |
| `CHARACTER SET utf8mb4` | `ENCODING 'UTF8'` | Postgres's UTF8 already covers full Unicode, no mb4 equivalent needed |
| Inline `CONSTRAINT ... FOREIGN KEY` | `REFERENCES` inline on the column | Both work in Postgres; inline is more idiomatic |
| `CHECK` as separate constraint | `CHECK` inline on column | Cleaner in Postgres |

All design decisions (RESTRICT vs CASCADE, indexing choices, `app_user` naming) carry over unchanged — the reasoning from Day 20 still applies.

---

## Table Row Count Estimates (unchanged from original Day 20)

| Table | Estimated rows |
|---|---|
| platform | 2 |
| category | 9 |
| product | 21,273 |
| sales | 21,273 |
| review | 20,333 |
| app_user | 0 initially |
