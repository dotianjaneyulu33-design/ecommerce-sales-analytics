# Database Schema Document (Day 20)
## Comparative Sales Analytics & Forecasting System

Database name: `ecommerce_analytics`
Engine: InnoDB (required for foreign key support)
Charset: `utf8mb4` (supports full Unicode, needed for product names/reviews with special characters, emoji, etc.)

---

## Full DDL

```sql
CREATE DATABASE IF NOT EXISTS ecommerce_analytics
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE ecommerce_analytics;

-- ========================================
-- 1. PLATFORM
-- ========================================
CREATE TABLE platform (
    platform_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ========================================
-- 2. CATEGORY
-- ========================================
CREATE TABLE category (
    category_id   INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ========================================
-- 3. PRODUCT
-- ========================================
CREATE TABLE product (
    product_pk       INT AUTO_INCREMENT PRIMARY KEY,
    id               VARCHAR(8) UNIQUE,
    platform_id      INT NOT NULL,
    category_id      INT NOT NULL,
    product_name     VARCHAR(500) NOT NULL,
    price            DECIMAL(10,2) NOT NULL,
    mrp              DECIMAL(10,2),
    discount_pct     DECIMAL(5,2),
    rating           DECIMAL(2,1),
    rating_count     INT DEFAULT 0,
    brand            VARCHAR(255),
    image_url        VARCHAR(500),
    source_url       VARCHAR(500),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_platform FOREIGN KEY (platform_id)
        REFERENCES platform(platform_id) ON DELETE RESTRICT,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id)
        REFERENCES category(category_id) ON DELETE RESTRICT,

    INDEX idx_product_platform (platform_id),
    INDEX idx_product_category (category_id),
    INDEX idx_product_rating (rating)
) ENGINE=InnoDB;

-- ========================================
-- 4. SALES
-- ========================================
CREATE TABLE sales (
    sale_id       INT AUTO_INCREMENT PRIMARY KEY,
    product_pk    INT NOT NULL,
    order_date    DATE NOT NULL,
    quantity      INT NOT NULL,
    revenue       DECIMAL(12,2) NOT NULL,

    CONSTRAINT fk_sales_product FOREIGN KEY (product_pk)
        REFERENCES product(product_pk) ON DELETE CASCADE,

    INDEX idx_sales_product (product_pk),
    INDEX idx_sales_date (order_date)
) ENGINE=InnoDB;

-- ========================================
-- 5. REVIEW
-- ========================================
CREATE TABLE review (
    review_pk        INT AUTO_INCREMENT PRIMARY KEY,
    product_pk        INT NOT NULL,
    reviewer_id       VARCHAR(100),
    reviewer_name     VARCHAR(255),
    review_title      VARCHAR(255),
    review_content    TEXT,
    sentiment         VARCHAR(20),
    is_fake           BOOLEAN,
    fake_confidence   DECIMAL(5,2),

    CONSTRAINT fk_review_product FOREIGN KEY (product_pk)
        REFERENCES product(product_pk) ON DELETE CASCADE,

    INDEX idx_review_product (product_pk),
    INDEX idx_review_sentiment (sentiment)
) ENGINE=InnoDB;

-- ========================================
-- 6. USER (application authentication)
-- ========================================
CREATE TABLE app_user (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(100) NOT NULL UNIQUE,
    password      VARCHAR(255) NOT NULL,
    role          VARCHAR(20) NOT NULL DEFAULT 'VIEWER',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_user_role CHECK (role IN ('ADMIN', 'VIEWER'))
) ENGINE=InnoDB;
```

---

## Design Decisions & Rationale

| Decision | Rationale |
|---|---|
| Table named `app_user`, not `user` | `USER` is a reserved word in MySQL — using it directly causes syntax errors without backtick-escaping everywhere. Avoiding the collision entirely is cleaner. |
| `ON DELETE RESTRICT` for Product's FKs | Prevents accidentally deleting a Platform or Category that still has products attached — forces explicit cleanup first. Protects data integrity. |
| `ON DELETE CASCADE` for Sales/Review's FKs | If a Product is deleted, its Sales and Review records are meaningless orphans — cascading delete keeps the DB clean automatically. |
| `rating DECIMAL(2,1)` | Matches the 0.0–5.0 rating range exactly (1 digit before decimal, 1 after) — no wasted storage. |
| Indexes on `platform_id`, `category_id`, `rating`, `order_date`, `sentiment` | These are the columns the dashboard will filter/group by constantly (Day 55-57, Day 81-83) — indexing them now avoids slow queries later. |
| `id VARCHAR(8) UNIQUE` on Product (separate from `product_pk`) | Keeps the original Day 14 generated ID for traceability back to source data, while `product_pk` serves as the clean auto-increment key Spring Data JPA will use internally. |
| `CHECK` constraint on `app_user.role` | Enforces only 'ADMIN' or 'VIEWER' at the database level, not just the application level — defense in depth. |

---

## Table Row Count Estimates (from Day 14 final data)

| Table | Estimated rows |
|---|---|
| platform | 2 |
| category | 9 |
| product | 21,273 |
| sales | 21,273 (1 per product initially) |
| review | 20,333 |
| app_user | 0 initially |

This schema is what Day 21-23 will actually execute in MySQL Workbench.
