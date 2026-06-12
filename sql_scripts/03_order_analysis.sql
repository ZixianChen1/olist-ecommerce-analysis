-- ============================================================
-- 03_order_analysis.sql
-- Order dimension analysis
-- ============================================================

-- 1. Total number of orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- 2. Order status distribution
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
        COUNT(*) * 1.0 / (SELECT COUNT(*) FROM orders),
        4
    ) AS order_ratio
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- 3. Daily order count
SELECT
    DATE(order_purchase_timestamp) AS order_date,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE(order_purchase_timestamp)
ORDER BY order_date;


-- 4. Weekly order count
SELECT
    STRFTIME('%Y-%W', order_purchase_timestamp) AS order_week,
    COUNT(*) AS order_count
FROM orders
GROUP BY STRFTIME('%Y-%W', order_purchase_timestamp)
ORDER BY order_week;


-- 5. Monthly order count
SELECT
    STRFTIME('%Y-%m', order_purchase_timestamp) AS order_month,
    COUNT(*) AS order_count
FROM orders
GROUP BY STRFTIME('%Y-%m', order_purchase_timestamp)
ORDER BY order_month;


-- 6. Order amount by order
-- total_order_amount = product price + freight
SELECT
    order_id,
    SUM(price) AS total_product_amount,
    SUM(freight_value) AS total_freight_amount,
    SUM(price + freight_value) AS total_order_amount
FROM order_items
GROUP BY order_id
ORDER BY total_order_amount DESC;


-- 7. Order amount distribution
-- SQLite does not have describe(), so we calculate basic statistics manually
SELECT
    COUNT(*) AS order_count,
    MIN(total_order_amount) AS min_order_amount,
    MAX(total_order_amount) AS max_order_amount,
    AVG(total_order_amount) AS avg_order_amount
FROM (
    SELECT
        order_id,
        SUM(price + freight_value) AS total_order_amount
    FROM order_items
    GROUP BY order_id
) AS order_amount;