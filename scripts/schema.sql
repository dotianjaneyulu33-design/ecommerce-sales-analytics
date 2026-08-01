-- Schema for project_DB (PostgreSQL)
-- Run this entire file in one go with:
-- "/c/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d project_DB -f schema.sql

-- Drop tables first in case of partial/previous attempts (safe - project_DB is currently empty)
DROP TABLE IF EXISTS review CASCADE;
DROP TABLE IF EXISTS sales CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS category CASCADE;
DROP TABLE IF EXISTS platform CASCADE;
DROP TABLE IF EXISTS app_user CASCADE;

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

-- Confirm success
\dt
