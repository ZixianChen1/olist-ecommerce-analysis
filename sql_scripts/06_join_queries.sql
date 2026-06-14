-- ============================================================
-- 06_join_queries.sql
-- Required join queries
-- ============================================================

-- 1. First and last purchase time of each customer
SELECT
    c.customer_unique_id,
    MIN(o.order_purchase_timestamp) AS first_purchase_time,
    MAX(o.order_purchase_timestamp) AS last_purchase_time,
    COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_unique_id
ORDER BY total_orders DESC;


-- 2. Seller city and total order volume
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(DISTINCT oi.order_id) AS total_order_count
FROM sellers s
LEFT JOIN order_items oi
    ON s.seller_id = oi.seller_id
GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY total_order_count DESC;


-- 3. Top 3 categories by sales volume in January 2018
-- Missing categories are labelled as 'Unknown'
SELECT
    COALESCE(p.product_category_name, 'Unknown') AS product_category_name,
    COUNT(*) AS sales_count
FROM orders o
INNER JOIN order_items oi
    ON o.order_id = oi.order_id
LEFT JOIN products p
    ON oi.product_id = p.product_id
WHERE o.order_purchase_timestamp >= '2018-01-01'
  AND o.order_purchase_timestamp < '2018-02-01'
GROUP BY COALESCE(p.product_category_name, 'Unknown')
ORDER BY sales_count DESC
LIMIT 3;