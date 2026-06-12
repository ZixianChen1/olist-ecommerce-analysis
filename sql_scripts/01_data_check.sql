-- ============================================================
-- 01_data_check.sql
-- Basic data check for 5 core tables
-- ============================================================

-- 1. Check row count of each table
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM orders
UNION ALL
SELECT 'order_items' AS table_name, COUNT(*) AS row_count FROM order_items
UNION ALL
SELECT 'products' AS table_name, COUNT(*) AS row_count FROM products
UNION ALL
SELECT 'sellers' AS table_name, COUNT(*) AS row_count FROM sellers;


-- 2. Check first 5 rows of customers
SELECT *
FROM customers
LIMIT 5;


-- 3. Check first 5 rows of orders
SELECT *
FROM orders
LIMIT 5;


-- 4. Check first 5 rows of order_items
SELECT *
FROM order_items
LIMIT 5;


-- 5. Check first 5 rows of products
SELECT *
FROM products
LIMIT 5;


-- 6. Check first 5 rows of sellers
SELECT *
FROM sellers
LIMIT 5;


-- 7. Check primary key uniqueness: customers
SELECT
    'customers' AS table_name,
    'customer_id' AS primary_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT customer_id) AS unique_values,
    CASE
        WHEN COUNT(*) = COUNT(DISTINCT customer_id) THEN 'True'
        ELSE 'False'
    END AS is_unique
FROM customers;


-- 8. Check primary key uniqueness: orders
SELECT
    'orders' AS table_name,
    'order_id' AS primary_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_values,
    CASE
        WHEN COUNT(*) = COUNT(DISTINCT order_id) THEN 'True'
        ELSE 'False'
    END AS is_unique
FROM orders;


-- 9. Check primary key uniqueness: products
SELECT
    'products' AS table_name,
    'product_id' AS primary_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_values,
    CASE
        WHEN COUNT(*) = COUNT(DISTINCT product_id) THEN 'True'
        ELSE 'False'
    END AS is_unique
FROM products;


-- 10. Check primary key uniqueness: sellers
SELECT
    'sellers' AS table_name,
    'seller_id' AS primary_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT seller_id) AS unique_values,
    CASE
        WHEN COUNT(*) = COUNT(DISTINCT seller_id) THEN 'True'
        ELSE 'False'
    END AS is_unique
FROM sellers;


-- 11. order_items has no single primary key
-- It is usually identified by order_id + order_item_id
SELECT
    'order_items' AS table_name,
    'order_id + order_item_id' AS composite_key,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id || '-' || order_item_id) AS unique_values,
    CASE
        WHEN COUNT(*) = COUNT(DISTINCT order_id || '-' || order_item_id) THEN 'True'
        ELSE 'False'
    END AS is_unique
FROM order_items;