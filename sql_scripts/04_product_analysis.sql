-- ============================================================
-- 04_product_analysis.sql
-- Product dimension analysis
-- ============================================================

-- 1. Total number of products and categories
SELECT
    COUNT(DISTINCT product_id) AS total_products,
    COUNT(DISTINCT product_category_name) AS total_categories
FROM products;


-- 2. Product count by category
SELECT
    product_category_name,
    COUNT(*) AS product_count
FROM products
GROUP BY product_category_name
ORDER BY product_count DESC;


-- 3. Product sales ranking
-- Each row in order_items represents one sold order item
SELECT
    product_id,
    COUNT(*) AS sales_count
FROM order_items
GROUP BY product_id
ORDER BY sales_count DESC;


-- 4. Category sales count
SELECT
    p.product_category_name,
    COUNT(*) AS sales_count
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY sales_count DESC;


-- 5. Category revenue ranking
SELECT
    p.product_category_name,
    SUM(oi.price) AS total_revenue,
    COUNT(oi.product_id) AS total_sales_count
FROM order_items oi
LEFT JOIN products p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_revenue DESC;