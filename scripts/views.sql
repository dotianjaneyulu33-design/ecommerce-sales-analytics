-- Day 28: Database Views for performance/reusability
-- Run with: "/c/Program Files/PostgreSQL/18/bin/psql.exe" -U postgres -d project_DB -f views.sql

DROP VIEW IF EXISTS v_platform_category_revenue;
DROP VIEW IF EXISTS v_product_summary;

-- View 1: Platform x Category revenue summary
CREATE VIEW v_platform_category_revenue AS
SELECT pl.name AS platform, c.name AS category,
       ROUND(SUM(s.revenue), 2) AS total_revenue,
       COUNT(DISTINCT p.product_pk) AS product_count,
       ROUND(AVG(p.rating), 2) AS avg_rating
FROM sales s
JOIN product p ON s.product_pk = p.product_pk
JOIN platform pl ON p.platform_id = pl.platform_id
JOIN category c ON p.category_id = c.category_id
GROUP BY pl.name, c.name;

-- View 2: Product summary with review counts
CREATE VIEW v_product_summary AS
SELECT p.product_pk, p.product_name, pl.name AS platform, c.name AS category,
       p.price, p.mrp, p.discount_pct, p.rating, p.rating_count, p.brand,
       COUNT(r.review_pk) AS review_count
FROM product p
JOIN platform pl ON p.platform_id = pl.platform_id
JOIN category c ON p.category_id = c.category_id
LEFT JOIN review r ON p.product_pk = r.product_pk
GROUP BY p.product_pk, p.product_name, pl.name, c.name, p.price, p.mrp, p.discount_pct, p.rating, p.rating_count, p.brand;

-- Confirm
\d v_platform_category_revenue
\d v_product_summary
