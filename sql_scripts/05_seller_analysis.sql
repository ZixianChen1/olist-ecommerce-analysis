-- ============================================================
-- 05_seller_analysis.sql
-- Seller dimension analysis
-- ============================================================

-- 1. Total number of sellers
SELECT
    COUNT(DISTINCT seller_id) AS total_sellers
FROM sellers;


-- 2. Seller distribution by state
SELECT
    seller_state,
    COUNT(*) AS seller_count
FROM sellers
GROUP BY seller_state
ORDER BY seller_count DESC;


-- 3. Seller order volume Top 10
-- unique_order_count means how many different orders each seller handled
SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(oi.order_id) AS order_item_count,
    COUNT(DISTINCT oi.order_id) AS unique_order_count
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY
    oi.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY unique_order_count DESC
LIMIT 10;


-- 4. Seller revenue Top 10
-- total_revenue is calculated by product price
SELECT
    oi.seller_id,
    s.seller_city,
    s.seller_state,
    SUM(oi.price) AS total_revenue,
    SUM(oi.freight_value) AS total_freight,
    COUNT(oi.order_id) AS order_item_count,
    COUNT(DISTINCT oi.order_id) AS unique_order_count
FROM order_items oi
LEFT JOIN sellers s
    ON oi.seller_id = s.seller_id
GROUP BY
    oi.seller_id,
    s.seller_city,
    s.seller_state
ORDER BY total_revenue DESC
LIMIT 10;