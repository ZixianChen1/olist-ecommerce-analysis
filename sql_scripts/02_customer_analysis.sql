-- ============================================================
-- 02_customer_analysis.sql
-- Customer dimension analysis
-- ============================================================

-- 1. Total number of customers
-- customer_id: order-level customer id
-- customer_unique_id: unique customer id
SELECT
    COUNT(DISTINCT customer_id) AS total_customer_id,
    COUNT(DISTINCT customer_unique_id) AS total_unique_customers
FROM customers;


-- 2. Customer distribution by state
SELECT
    customer_state,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_state
ORDER BY customer_count DESC;


-- 3. Customer distribution by city
SELECT
    customer_city,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_city
ORDER BY customer_count DESC;


-- 4. Orders per customer
-- Count how many orders each customer has
SELECT
    customer_id,
    COUNT(order_id) AS order_count
FROM orders
GROUP BY customer_id
ORDER BY order_count DESC;


-- 5. Orders per customer distribution
-- Count how many customers placed 1 order, 2 orders, etc.
SELECT
    order_count,
    COUNT(*) AS customer_count
FROM (
    SELECT
        customer_id,
        COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
) AS customer_order_count
GROUP BY order_count
ORDER BY order_count;